#!/usr/bin/env python3
"""
IPFS 업로드 유틸리티
다양한 IPFS 서비스 지원 (Pinata, Infura, Web3.Storage)
"""

import json
import os
import requests
import base64
from typing import Dict, Any, Optional, Union
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class IPFSUploader:
    def __init__(self, service: str = "pinata", **kwargs):
        """
        IPFS 업로더 초기화
        
        Args:
            service: IPFS 서비스 ("pinata", "infura", "web3storage")
            **kwargs: 서비스별 인증 정보
        """
        self.service = service.lower()
        self.auth_info = kwargs
        
        if self.service == "pinata":
            self.api_key = kwargs.get("api_key")
            self.secret_key = kwargs.get("secret_key")
            if not self.api_key or not self.secret_key:
                raise ValueError("Pinata requires api_key and secret_key")
                
        elif self.service == "infura":
            self.project_id = kwargs.get("project_id")
            self.project_secret = kwargs.get("project_secret")
            if not self.project_id or not self.project_secret:
                raise ValueError("Infura requires project_id and project_secret")
                
        elif self.service == "web3storage":
            self.api_token = kwargs.get("api_token")
            if not self.api_token:
                raise ValueError("Web3.Storage requires api_token")
        else:
            raise ValueError(f"Unsupported service: {service}")
    
    def upload_json(self, data: Dict[str, Any], filename: Optional[str] = None) -> str:
        """
        JSON 데이터를 IPFS에 업로드
        
        Args:
            data: 업로드할 JSON 데이터
            filename: 파일명 (선택사항)
            
        Returns:
            IPFS URL (ipfs://...)
        """
        if filename is None:
            filename = f"metadata_{int(time.time())}.json"
            
        json_str = json.dumps(data, ensure_ascii=False, indent=2)
        
        if self.service == "pinata":
            return self._upload_to_pinata_json(json_str, filename)
        elif self.service == "infura":
            return self._upload_to_infura_json(json_str, filename)
        elif self.service == "web3storage":
            return self._upload_to_web3storage_json(json_str, filename)
    
    def upload_file(self, file_path: Union[str, Path]) -> str:
        """
        파일을 IPFS에 업로드
        
        Args:
            file_path: 업로드할 파일 경로
            
        Returns:
            IPFS URL (ipfs://...)
        """
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
            
        if self.service == "pinata":
            return self._upload_to_pinata_file(file_path)
        elif self.service == "infura":
            return self._upload_to_infura_file(file_path)
        elif self.service == "web3storage":
            return self._upload_to_web3storage_file(file_path)
    
    def _upload_to_pinata_json(self, json_str: str, filename: str) -> str:
        """Pinata에 JSON 업로드"""
        try:
            url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
            headers = {
                'pinata_api_key': self.api_key,
                'pinata_secret_api_key': self.secret_key
            }
            
            files = {
                'file': (filename, json_str, 'application/json')
            }
            
            response = requests.post(url, files=files, headers=headers)
            response.raise_for_status()
            
            ipfs_hash = response.json()['IpfsHash']
            ipfs_url = f"ipfs://{ipfs_hash}"
            
            logger.info(f"✅ Pinata 업로드 성공: {ipfs_url}")
            return ipfs_url
            
        except Exception as e:
            logger.error(f"❌ Pinata 업로드 실패: {e}")
            raise
    
    def _upload_to_pinata_file(self, file_path: Path) -> str:
        """Pinata에 파일 업로드"""
        try:
            url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
            headers = {
                'pinata_api_key': self.api_key,
                'pinata_secret_api_key': self.secret_key
            }
            
            with open(file_path, 'rb') as f:
                files = {'file': (file_path.name, f, 'application/octet-stream')}
                response = requests.post(url, files=files, headers=headers)
            
            response.raise_for_status()
            
            ipfs_hash = response.json()['IpfsHash']
            ipfs_url = f"ipfs://{ipfs_hash}"
            
            logger.info(f"✅ Pinata 파일 업로드 성공: {ipfs_url}")
            return ipfs_url
            
        except Exception as e:
            logger.error(f"❌ Pinata 파일 업로드 실패: {e}")
            raise
    
    def _upload_to_infura_json(self, json_str: str, filename: str) -> str:
        """Infura IPFS에 JSON 업로드"""
        try:
            url = "https://ipfs.infura.io:5001/api/v0/add"
            
            # Basic auth 설정
            auth = (self.project_id, self.project_secret)
            
            files = {
                'file': (filename, json_str, 'application/json')
            }
            
            response = requests.post(url, files=files, auth=auth)
            response.raise_for_status()
            
            result = response.json()
            ipfs_hash = result['Hash']
            ipfs_url = f"ipfs://{ipfs_hash}"
            
            logger.info(f"✅ Infura 업로드 성공: {ipfs_url}")
            return ipfs_url
            
        except Exception as e:
            logger.error(f"❌ Infura 업로드 실패: {e}")
            raise
    
    def _upload_to_infura_file(self, file_path: Path) -> str:
        """Infura IPFS에 파일 업로드"""
        try:
            url = "https://ipfs.infura.io:5001/api/v0/add"
            auth = (self.project_id, self.project_secret)
            
            with open(file_path, 'rb') as f:
                files = {'file': (file_path.name, f)}
                response = requests.post(url, files=files, auth=auth)
            
            response.raise_for_status()
            
            result = response.json()
            ipfs_hash = result['Hash']
            ipfs_url = f"ipfs://{ipfs_hash}"
            
            logger.info(f"✅ Infura 파일 업로드 성공: {ipfs_url}")
            return ipfs_url
            
        except Exception as e:
            logger.error(f"❌ Infura 파일 업로드 실패: {e}")
            raise
    
    def _upload_to_web3storage_json(self, json_str: str, filename: str) -> str:
        """Web3.Storage에 JSON 업로드"""
        try:
            url = "https://api.web3.storage/upload"
            headers = {
                'Authorization': f'Bearer {self.api_token}',
                'Content-Type': 'application/json'
            }
            
            # Web3.Storage는 다른 형식을 요구할 수 있음
            files = {
                'file': (filename, json_str, 'application/json')
            }
            
            response = requests.post(url, files=files, headers=headers)
            response.raise_for_status()
            
            result = response.json()
            cid = result['cid']
            ipfs_url = f"ipfs://{cid}"
            
            logger.info(f"✅ Web3.Storage 업로드 성공: {ipfs_url}")
            return ipfs_url
            
        except Exception as e:
            logger.error(f"❌ Web3.Storage 업로드 실패: {e}")
            raise
    
    def _upload_to_web3storage_file(self, file_path: Path) -> str:
        """Web3.Storage에 파일 업로드"""
        try:
            url = "https://api.web3.storage/upload"
            headers = {
                'Authorization': f'Bearer {self.api_token}'
            }
            
            with open(file_path, 'rb') as f:
                files = {'file': (file_path.name, f)}
                response = requests.post(url, files=files, headers=headers)
            
            response.raise_for_status()
            
            result = response.json()
            cid = result['cid']
            ipfs_url = f"ipfs://{cid}"
            
            logger.info(f"✅ Web3.Storage 파일 업로드 성공: {ipfs_url}")
            return ipfs_url
            
        except Exception as e:
            logger.error(f"❌ Web3.Storage 파일 업로드 실패: {e}")
            raise

def create_metadata_with_template(energy_data: Dict[str, Any], template_path: str = "utils/metadata_templates.json") -> Dict[str, Any]:
    """
    템플릿을 사용하여 메타데이터 생성
    
    Args:
        energy_data: 에너지 거래 데이터
        template_path: 템플릿 파일 경로
        
    Returns:
        생성된 메타데이터
    """
    # 템플릿 로드
    with open(template_path, 'r', encoding='utf-8') as f:
        templates = json.load(f)
    
    energy_type = energy_data['energy_type']
    if energy_type not in templates['templates']:
        raise ValueError(f"지원되지 않는 에너지 타입: {energy_type}")
    
    template = templates['templates'][energy_type]
    
    # 탄소 회피량 계산
    carbon_offset = energy_data['energy_amount'] * template['carbon_factor']
    
    # 템플릿 변수 치환
    metadata = {
        "name": template['name'].format(
            tokenId=energy_data.get('token_id', 'TBD')
        ),
        "description": template['description'].format(
            energyAmount=energy_data['energy_amount']
        ),
        "image": template['image'],
        "external_url": f"https://energy-nft.com/token/{energy_data.get('token_id', '')}",
        "attributes": [],
        "properties": {}
    }
    
    # 속성 추가
    for attr in template['attributes']:
        new_attr = attr.copy()
        if isinstance(attr['value'], str) and '{' in attr['value']:
            new_attr['value'] = attr['value'].format(**energy_data)
        metadata['attributes'].append(new_attr)
    
    # 공통 속성 추가
    for attr in templates['common_attributes']:
        new_attr = attr.copy()
        if attr['trait_type'] == '탄소 회피량 (tCO₂)':
            new_attr['value'] = round(carbon_offset, 3)
        elif isinstance(attr['value'], str) and '{' in attr['value']:
            value_str = attr['value']
            if '{carbonOffset}' in value_str:
                value_str = value_str.replace('{carbonOffset}', str(round(carbon_offset, 3)))
            new_attr['value'] = value_str.format(**energy_data)
        metadata['attributes'].append(new_attr)
    
    # 속성 정보 설정
    properties_template = templates['properties_template']
    for key, value in properties_template.items():
        if isinstance(value, str) and '{' in value:
            if '{carbonOffset}' in value:
                value = value.replace('{carbonOffset}', str(carbon_offset))
            metadata['properties'][key] = value.format(**energy_data)
        else:
            metadata['properties'][key] = value
    
    return metadata

# 사용 예시
if __name__ == "__main__":
    import time
    
    # Pinata 업로더 테스트
    uploader = IPFSUploader(
        service="pinata",
        api_key="YOUR_API_KEY",
        secret_key="YOUR_SECRET_KEY"
    )
    
    # 샘플 에너지 데이터
    sample_data = {
        "energy_amount": 1.5,
        "energy_type": "solar",
        "supplier": "0x742d35Cc6634C0532925a3b8D7e99B8fF4b4c4C7",
        "buyer": "0x8ba1f109551bD432803012645Hac136c903C2B3F",
        "location": "경기도 화성시 태양광발전소",
        "timestamp": time.time(),
        "country": "South Korea",
        "year": 2024
    }
    
    # 메타데이터 생성 및 업로드
    try:
        metadata = create_metadata_with_template(sample_data)
        ipfs_url = uploader.upload_json(metadata)
        print(f"🎉 메타데이터 업로드 완료: {ipfs_url}")
    except Exception as e:
        print(f"❌ 업로드 실패: {e}")