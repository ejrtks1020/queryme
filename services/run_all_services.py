#!/usr/bin/env python3
"""
QueryMe 모든 서비스를 uv run으로 멀티프로세스 실행하는 스크립트
로그 스트리밍 기능 포함
"""

import os
import sys
import time
import signal
import subprocess
import multiprocessing
import threading
import queue
from pathlib import Path
from typing import Dict, List
import logging
from datetime import datetime

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ANSI 색상 코드
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    GRAY = "\033[90m"

class LogStreamer:
    """로그 스트리밍을 위한 클래스"""
    
    def __init__(self, service_name: str, stream, log_queue: queue.Queue, color: str):
        self.service_name = service_name
        self.stream = stream
        self.log_queue = log_queue
        self.color = color
        self.running = True
        
    def stream_logs(self):
        """로그를 스트리밍"""
        try:
            for line in iter(self.stream.readline, ''):
                if not self.running:
                    break
                if line:
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    formatted_line = f"{self.color}[{timestamp}] {self.service_name}:{Colors.RESET} {line.rstrip()}"
                    self.log_queue.put(formatted_line)
        except Exception as e:
            error_line = f"{Colors.RED}[ERROR] {self.service_name} 로그 스트리밍 오류: {e}{Colors.RESET}"
            self.log_queue.put(error_line)

class ServiceManager:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.services_root = self.project_root
        self.processes: Dict[str, subprocess.Popen] = {}
        self.log_streamers: Dict[str, List[LogStreamer]] = {}
        self.log_queue = queue.Queue()
        self.log_thread = None
        self.service_configs = {
            "auth_service": {
                "path": "auth_service/app",
                "port": 8081,
                "env": {"PROFILE": "local"},
                "color": Colors.BLUE
            },
            "connection_service": {
                "path": "connection_service/app", 
                "port": 8082,
                "env": {"PROFILE": "local"},
                "color": Colors.GREEN
            },
            "ddl_session_service": {
                "path": "ddl_session_service/app",
                "port": 8084, 
                "env": {"PROFILE": "local"},
                "color": Colors.YELLOW
            },
            "history_service": {
                "path": "history_service/app",
                "port": 8085,
                "env": {"PROFILE": "local"},
                "color": Colors.MAGENTA
            },
            "nl2sql_service": {
                "path": "nl2sql_service/app",
                "port": 8083,
                "env": {"PROFILE": "local"},
                "color": Colors.CYAN
            },
            "gateway": {
                "path": "gateway/app",
                "port": 8080,
                "env": {"PROFILE": "local"},
                "color": Colors.RED
            }
        }
        
    def check_uv_installed(self) -> bool:
        """uv가 설치되어 있는지 확인"""
        try:
            result = subprocess.run(["uv", "--version"], 
                                  capture_output=True, text=True, check=True)
            logger.info(f"{Colors.GREEN}✅ uv 버전: {result.stdout.strip()}{Colors.RESET}")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.error(f"{Colors.RED}❌ uv가 설치되어 있지 않습니다. https://docs.astral.sh/uv/getting-started/installation/ 에서 설치하세요.{Colors.RESET}")
            return False
    
    def start_log_consumer(self):
        """로그 소비자 스레드 시작"""
        def consume_logs():
            while True:
                try:
                    log_line = self.log_queue.get(timeout=1)
                    if log_line == "STOP":
                        break
                    print(log_line)
                except queue.Empty:
                    continue
                except Exception as e:
                    print(f"{Colors.RED}로그 소비 중 오류: {e}{Colors.RESET}")
        
        self.log_thread = threading.Thread(target=consume_logs, daemon=True)
        self.log_thread.start()
    
    def stop_log_consumer(self):
        """로그 소비자 스레드 중지"""
        if self.log_queue:
            self.log_queue.put("STOP")
        if self.log_thread:
            self.log_thread.join(timeout=2)
        
    def start_service(self, service_name: str) -> bool:
        """개별 서비스 시작"""
        if service_name not in self.service_configs:
            logger.error(f"{Colors.RED}알 수 없는 서비스: {service_name}{Colors.RESET}")
            return False
            
        config = self.service_configs[service_name]
        service_path = self.services_root / config["path"]
        
        if not service_path.exists():
            logger.error(f"{Colors.RED}서비스 경로가 존재하지 않습니다: {service_path}{Colors.RESET}")
            return False
            
        # main.py 파일 존재 확인
        main_file = service_path / "main.py"
        if not main_file.exists():
            logger.error(f"{Colors.RED}main.py 파일이 존재하지 않습니다: {main_file}{Colors.RESET}")
            return False
        
        # 환경 변수 설정
        env = os.environ.copy()
        env.update(config["env"])
        env["PYTHONPATH"] = str(self.services_root)  # 이 줄 추가
        
        try:
            # 루트에서 uv run으로 서비스 시작 (모노레포 구조)
            main_script = f"{config['path']}/main.py"
            process = subprocess.Popen(
                ["uv", "run", main_script],
                cwd=self.services_root,  # 루트 디렉토리에서 실행
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,  # stderr를 stdout으로 리다이렉트
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            self.processes[service_name] = process
            
            # 로그 스트리머 시작 (색상 전달)
            log_streamer = LogStreamer(service_name, process.stdout, self.log_queue, config["color"])
            self.log_streamers[service_name] = [log_streamer]
            
            log_thread = threading.Thread(
                target=log_streamer.stream_logs, 
                daemon=True
            )
            log_thread.start()
            
            logger.info(f"{config['color']}✅ {service_name} 시작됨 (PID: {process.pid}, Port: {config['port']}){Colors.RESET}")
            
            # 서비스가 완전히 시작될 때까지 잠시 대기
            time.sleep(3)
            
            # 프로세스가 살아있는지 확인
            if process.poll() is None:
                return True
            else:
                logger.error(f"{Colors.RED}❌ {service_name} 시작 실패{Colors.RESET}")
                return False
                
        except Exception as e:
            logger.error(f"{Colors.RED}❌ {service_name} 시작 중 오류: {e}{Colors.RESET}")
            return False
    
    def start_all_services(self) -> bool:
        """모든 서비스 시작"""
        logger.info(f"{Colors.CYAN}🚀 QueryMe 모든 서비스 시작 중... (모노레포 구조){Colors.RESET}")
        
        # uv 설치 확인
        if not self.check_uv_installed():
            return False
        
        # 루트 pyproject.toml 파일 존재 확인
        root_pyproject = self.services_root / "pyproject.toml"
        if not root_pyproject.exists():
            logger.error(f"{Colors.RED}❌ 루트 pyproject.toml 파일이 존재하지 않습니다: {root_pyproject}{Colors.RESET}")
            return False
        
        # 로그 소비자 시작
        self.start_log_consumer()
        
        # Gateway를 마지막에 시작 (다른 서비스들이 먼저 시작되어야 함)
        service_order = [
            "auth_service",
            "connection_service", 
            "ddl_session_service",
            "history_service",
            "nl2sql_service",
            "gateway"
        ]
        
        success_count = 0
        for service_name in service_order:
            config = self.service_configs[service_name]
            logger.info(f"{config['color']}🔄 {service_name} 시작 중...{Colors.RESET}")
            if self.start_service(service_name):
                success_count += 1
                logger.info(f"{config['color']}✅ {service_name} 시작 완료{Colors.RESET}")
            else:
                logger.error(f"{Colors.RED}❌ {service_name} 시작 실패로 인해 중단{Colors.RESET}")
                self.stop_all_services()
                return False
        
        logger.info(f"{Colors.GREEN}✅ {success_count}/{len(service_order)} 서비스가 성공적으로 시작되었습니다!{Colors.RESET}")
        logger.info(f"{Colors.CYAN}📝 모든 서비스가 루트 pyproject.toml의 의존성을 공유합니다.{Colors.RESET}")
        return True
    
    def stop_service(self, service_name: str):
        """개별 서비스 중지"""
        if service_name in self.processes:
            process = self.processes[service_name]
            config = self.service_configs[service_name]
            
            # 로그 스트리머 중지
            if service_name in self.log_streamers:
                for streamer in self.log_streamers[service_name]:
                    streamer.running = False
                del self.log_streamers[service_name]
            
            try:
                logger.info(f"{config['color']}🛑 {service_name} 중지 중...{Colors.RESET}")
                process.terminate()
                process.wait(timeout=10)
                logger.info(f"{config['color']}✅ {service_name} 중지됨{Colors.RESET}")
            except subprocess.TimeoutExpired:
                logger.warning(f"{Colors.YELLOW}⚠️ {service_name} 강제 종료 중...{Colors.RESET}")
                process.kill()
                process.wait()
                logger.warning(f"{Colors.YELLOW}⚠️ {service_name} 강제 종료됨{Colors.RESET}")
            except Exception as e:
                logger.error(f"{Colors.RED}❌ {service_name} 중지 중 오류: {e}{Colors.RESET}")
            finally:
                del self.processes[service_name]
    
    def stop_all_services(self):
        """모든 서비스 중지"""
        logger.info(f"{Colors.YELLOW}🛑 모든 서비스 중지 중...{Colors.RESET}")
        
        # Gateway를 먼저 중지
        stop_order = [
            "gateway",
            "nl2sql_service",
            "history_service", 
            "ddl_session_service",
            "connection_service",
            "auth_service"
        ]
        
        for service_name in stop_order:
            if service_name in self.processes:
                self.stop_service(service_name)
        
        # 로그 소비자 중지
        self.stop_log_consumer()
        
        logger.info(f"{Colors.GREEN}✅ 모든 서비스가 중지되었습니다.{Colors.RESET}")
    
    def check_services_status(self):
        """서비스 상태 확인"""
        logger.info(f"\n{Colors.CYAN}📊 서비스 상태:{Colors.RESET}")
        logger.info("-" * 60)
        
        for service_name, config in self.service_configs.items():
            if service_name in self.processes:
                process = self.processes[service_name]
                if process.poll() is None:
                    logger.info(f"{config['color']}✅ {service_name}: 실행 중 (PID: {process.pid}, Port: {config['port']}){Colors.RESET}")
                else:
                    logger.info(f"{Colors.RED}❌ {service_name}: 중지됨{Colors.RESET}")
            else:
                logger.info(f"{Colors.GRAY}❌ {service_name}: 시작되지 않음{Colors.RESET}")
        
        logger.info("-" * 60)
    
    def run_interactive(self):
        """대화형 모드로 실행"""
        try:
            if self.start_all_services():
                logger.info(f"\n{Colors.GREEN} 모든 서비스가 성공적으로 시작되었습니다!{Colors.RESET}")
                logger.info(f"{Colors.CYAN}📋 모노레포 구조: 모든 서비스가 루트 pyproject.toml을 공유합니다.{Colors.RESET}")
                logger.info(f"{Colors.CYAN} 사용 가능한 명령어:{Colors.RESET}")
                logger.info("  status - 서비스 상태 확인")
                logger.info("  stop   - 모든 서비스 중지")
                logger.info("  quit   - 종료")
                logger.info(f"\n{Colors.CYAN} 각 서비스의 로그가 실시간으로 표시됩니다.{Colors.RESET}")
                
                while True:
                    try:
                        command = input(f"\n{Colors.YELLOW}명령어 입력 (status/stop/quit): {Colors.RESET}").strip().lower()
                        
                        if command == "status":
                            self.check_services_status()
                        elif command == "stop":
                            self.stop_all_services()
                            break
                        elif command == "quit":
                            break
                        else:
                            logger.info(f"{Colors.YELLOW}알 수 없는 명령어입니다. status/stop/quit 중 하나를 입력하세요.{Colors.RESET}")
                            
                    except KeyboardInterrupt:
                        break
                        
        except KeyboardInterrupt:
            logger.info(f"\n{Colors.YELLOW}⚠️ 사용자에 의해 중단됨{Colors.RESET}")
        finally:
            self.stop_all_services()

def signal_handler(signum, frame):
    """시그널 핸들러"""
    logger.info(f"\n{Colors.YELLOW}⚠️ 시그널 {signum} 수신됨. 모든 서비스를 중지합니다...{Colors.RESET}")
    if hasattr(signal_handler, 'service_manager'):
        signal_handler.service_manager.stop_all_services()
    sys.exit(0)

def main():
    """메인 함수"""
    # 시그널 핸들러 등록
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    service_manager = ServiceManager()
    signal_handler.service_manager = service_manager
    
    # 명령행 인수 처리
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "start":
            service_manager.start_all_services()
        elif command == "stop":
            service_manager.stop_all_services()
        elif command == "status":
            service_manager.check_services_status()
        elif command == "restart":
            service_manager.stop_all_services()
            time.sleep(2)
            service_manager.start_all_services()
        else:
            logger.error(f"{Colors.RED}알 수 없는 명령어입니다. start/stop/status/restart 중 하나를 사용하세요.{Colors.RESET}")
    else:
        # 대화형 모드
        service_manager.run_interactive()

if __name__ == "__main__":
    main()