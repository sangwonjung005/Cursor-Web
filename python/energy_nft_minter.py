#!/usr/bin/env python3
"""
에너지 인증서 NFT 자동 민팅 스크립트
RE100, CBAM, 탄소거래용 NFT 생성 및 관리
"""

import json
import os
import requests
import time
from datetime import datetime
from typing import Dict, Any, Optional
from web3 import Web3
from eth_account import Account
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EnergyNFTMinter:
    def __init__(self, config_path: str = "config.json"):
        """
        에너지 NFT 민터 초기화
        Args:
            config_path: 설정 파일 경로
        """
        self.config = self.load_config(config_path)
        self.w3 = self.setup_web3()
        self.contract = self.setup_contract()
        self.account = Account.from_key(self.config['private_key'])
        
    def load_config(self, config_path: str) -> Dict[str, Any]:
        """설정 파일 로드"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            logger.info("✅ 설정 파일 로드 완료")
            return config
        except FileNotFoundError:
            logger.error("❌ 설정 파일을 찾을 수 없습니다. config.json을 생성해주세요.")
            raise
            
    def setup_web3(self) -> Web3:
        """Web3 연결 설정"""
        w3 = Web3(Web3.HTTPProvider(self.config['rpc_url']))
        if not w3.is_connected():
            raise ConnectionError("❌ 블록체인 네트워크에 연결할 수 없습니다.")
        logger.info(f"✅ {self.config['network']} 네트워크 연결 완료")
        return w3
        
    def setup_contract(self) -> Any:
        """스마트컨트랙트 설정"""
        try:
            with open(self.config['contract_abi_path'], 'r') as f:
                abi = json.load(f)
            
            contract = self.w3.eth.contract(
                address=self.config['contract_address'],
                abi=abi
            )
            logger.info("✅ 스마트컨트랙트 연결 완료")
            return contract
        except Exception as e:
            logger.error(f"❌ 컨트랙트 설정 실패: {e}")
            raise
            
    def generate_metadata(self, energy_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        에너지 거래 데이터를 기반으로 NFT 메타데이터 생성
        Args:
            energy_data: 에너지 거래 정보
        Returns:
            NFT 메타데이터 딕셔너리
        """
        # 탄소 회피량 계산 (태양광: 0.466 tCO2/MWh, 풍력: 0.011 tCO2/MWh)
        carbon_factors = {
            'solar': 0.466,
            'wind': 0.011,
            'hydro': 0.024,
            'biomass': 0.18
        }
        
        carbon_offset = energy_data['energy_amount'] * carbon_factors.get(
            energy_data['energy_type'], 0.4
        )
        
        metadata = {
            "name": f"RE100 전력 NFT #{energy_data.get('token_id', 'TBD')}",
            "description": f"{energy_data['energy_amount']}MWh {energy_data['energy_type']} 전력 거래 인증서",
            "image": self.get_energy_type_image(energy_data['energy_type']),
            "external_url": f"https://energy-nft.com/token/{energy_data.get('token_id', '')}",
            "attributes": [
                {
                    "trait_type": "전력량 (MWh)",
                    "value": energy_data['energy_amount'],
                    "display_type": "number"
                },
                {
                    "trait_type": "에너지 타입",
                    "value": energy_data['energy_type']
                },
                {
                    "trait_type": "거래일시",
                    "value": energy_data.get('timestamp', datetime.now().isoformat())
                },
                {
                    "trait_type": "공급자",
                    "value": energy_data['supplier']
                },
                {
                    "trait_type": "수요자",
                    "value": energy_data['buyer']
                },
                {
                    "trait_type": "발전소 위치",
                    "value": energy_data['location']
                },
                {
                    "trait_type": "탄소 회피량 (tCO₂)",
                    "value": round(carbon_offset, 3),
                    "display_type": "number"
                },
                {
                    "trait_type": "RE100 적합성",
                    "value": "인증됨"
                },
                {
                    "trait_type": "CBAM 대응",
                    "value": "적합"
                }
            ],
            "properties": {
                "category": "Energy Certificate",
                "subcategory": energy_data['energy_type'].title(),
                "is_renewable": True,
                "certification_standard": "RE100",
                "carbon_offset_tco2": carbon_offset,
                "energy_amount_mwh": energy_data['energy_amount']
            }
        }
        
        return metadata
        
    def get_energy_type_image(self, energy_type: str) -> str:
        """에너지 타입별 이미지 URL 반환"""
        image_mapping = {
            'solar': 'ipfs://QmSolarPanelIcon/solar.png',
            'wind': 'ipfs://QmWindTurbineIcon/wind.png',
            'hydro': 'ipfs://QmHydroIcon/hydro.png',
            'biomass': 'ipfs://QmBiomassIcon/biomass.png'
        }
        return image_mapping.get(energy_type, 'ipfs://QmDefaultEnergyIcon/default.png')
        
    def upload_to_ipfs(self, metadata: Dict[str, Any]) -> str:
        """
        메타데이터를 IPFS에 업로드 (Pinata 서비스 사용)
        Args:
            metadata: 업로드할 메타데이터
        Returns:
            IPFS 해시 (ipfs:// 형식)
        """
        try:
            # 임시 파일로 메타데이터 저장
            filename = f"metadata_{int(time.time())}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, ensure_ascii=False, indent=2)
            
            # Pinata API를 통해 IPFS 업로드
            url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
            headers = {
                'pinata_api_key': self.config['pinata_api_key'],
                'pinata_secret_api_key': self.config['pinata_secret_key']
            }
            
            with open(filename, 'rb') as f:
                files = {'file': f}
                response = requests.post(url, files=files, headers=headers)
            
            # 임시 파일 삭제
            os.remove(filename)
            
            if response.status_code == 200:
                ipfs_hash = response.json()['IpfsHash']
                ipfs_url = f"ipfs://{ipfs_hash}"
                logger.info(f"✅ IPFS 업로드 완료: {ipfs_url}")
                return ipfs_url
            else:
                raise Exception(f"IPFS 업로드 실패: {response.text}")
                
        except Exception as e:
            logger.error(f"❌ IPFS 업로드 오류: {e}")
            raise
            
    def mint_nft(self, energy_data: Dict[str, Any]) -> str:
        """
        에너지 NFT 민팅
        Args:
            energy_data: 에너지 거래 데이터
        Returns:
            트랜잭션 해시
        """
        try:
            logger.info("🚀 NFT 민팅 시작...")
            
            # 1. 메타데이터 생성
            metadata = self.generate_metadata(energy_data)
            logger.info("📄 메타데이터 생성 완료")
            
            # 2. IPFS 업로드
            token_uri = self.upload_to_ipfs(metadata)
            
            # 3. 탄소 회피량 계산
            carbon_factors = {'solar': 0.466, 'wind': 0.011, 'hydro': 0.024, 'biomass': 0.18}
            carbon_offset = int(energy_data['energy_amount'] * carbon_factors.get(
                energy_data['energy_type'], 0.4
            ) * 1000)  # 소수점 3자리까지 정수로 변환
            
            # 4. 스마트컨트랙트 함수 호출 준비
            recipient = energy_data['buyer']
            energy_amount = int(energy_data['energy_amount'] * 1000)  # MWh를 kWh로 변환
            supplier = energy_data['supplier']
            buyer = energy_data['buyer']
            energy_type = energy_data['energy_type']
            location = energy_data['location']
            
            # 5. 트랜잭션 빌드
            nonce = self.w3.eth.get_transaction_count(self.account.address)
            
            transaction = self.contract.functions.mintEnergyNFT(
                recipient,
                token_uri,
                energy_amount,
                supplier,
                buyer,
                energy_type,
                carbon_offset,
                location
            ).build_transaction({
                'from': self.account.address,
                'nonce': nonce,
                'gas': 500000,
                'gasPrice': self.w3.to_wei('10', 'gwei')
            })
            
            # 6. 트랜잭션 서명 및 전송
            signed_txn = self.w3.eth.account.sign_transaction(transaction, self.config['private_key'])
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            
            logger.info(f"✅ 민팅 트랜잭션 전송 완료: {self.w3.to_hex(tx_hash)}")
            
            # 7. 트랜잭션 확인 대기
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            if receipt.status == 1:
                logger.info(f"🎉 NFT 민팅 성공! Gas 사용량: {receipt.gasUsed}")
                return self.w3.to_hex(tx_hash)
            else:
                raise Exception("트랜잭션 실패")
                
        except Exception as e:
            logger.error(f"❌ NFT 민팅 실패: {e}")
            raise
            
    def batch_mint(self, energy_data_list: list) -> list:
        """
        배치 민팅 (여러 NFT 한 번에 민팅)
        Args:
            energy_data_list: 에너지 데이터 리스트
        Returns:
            트랜잭션 해시 리스트
        """
        results = []
        for i, energy_data in enumerate(energy_data_list):
            try:
                logger.info(f"📦 배치 민팅 진행 중... ({i+1}/{len(energy_data_list)})")
                tx_hash = self.mint_nft(energy_data)
                results.append({'success': True, 'tx_hash': tx_hash, 'data': energy_data})
                
                # API 레이트 리미트 방지를 위한 대기
                time.sleep(2)
                
            except Exception as e:
                logger.error(f"❌ 배치 민팅 {i+1}번 실패: {e}")
                results.append({'success': False, 'error': str(e), 'data': energy_data})
                
        return results


def main():
    """메인 실행 함수"""
    try:
        # NFT 민터 초기화
        minter = EnergyNFTMinter("config.json")
        
        # 예시 에너지 거래 데이터
        sample_energy_data = {
            "energy_amount": 1.5,  # 1.5 MWh
            "energy_type": "solar",
            "supplier": "0x742d35Cc6634C0532925a3b8D7e99B8fF4b4c4C7",
            "buyer": "0x8ba1f109551bD432803012645Hac136c903C2B3F",
            "location": "경기도 화성시 태양광발전소",
            "timestamp": datetime.now().isoformat()
        }
        
        # NFT 민팅 실행
        tx_hash = minter.mint_nft(sample_energy_data)
        print(f"🎉 NFT 민팅 완료! 트랜잭션 해시: {tx_hash}")
        
    except Exception as e:
        logger.error(f"❌ 프로그램 실행 실패: {e}")


if __name__ == "__main__":
    main()