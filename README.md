# 🌱 Energy Certificate NFT

**RE100, CBAM, 탄소거래를 위한 에너지 인증서 NFT 플랫폼**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Solidity](https://img.shields.io/badge/Solidity-%5E0.8.19-blue)](https://docs.soliditylang.org)
[![Hardhat](https://img.shields.io/badge/Hardhat-2.19.0-yellow)](https://hardhat.org)
[![Node.js](https://img.shields.io/badge/Node.js-16%2B-green)](https://nodejs.org)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)

## 📋 프로젝트 개요

Energy Certificate NFT는 재생에너지 전력 거래를 블록체인으로 투명하게 관리하고, RE100 이니셔티브와 CBAM(탄소국경조정메커니즘) 규제에 대응하기 위한 NFT 기반 플랫폼입니다.

### ✨ 주요 특징

- **🔐 ERC-721 기반**: OpenZeppelin 표준 라이브러리 활용으로 안전성 보장
- **🌍 다양한 에너지원 지원**: 태양광, 풍력, 수력, 바이오매스 등
- **📊 탄소 회피량 자동 계산**: 에너지 타입별 탄소 배출 계수 적용
- **♻️ NFT 은퇴 시스템**: 중복 사용 방지를 위한 크레딧 소각 기능
- **🔍 투명한 거래 추적**: 공급자, 수요자, 거래 시간 등 모든 정보 기록
- **🛡️ 접근 제어**: 관리자 전용 민팅 및 일시정지 기능
- **📱 다중 플랫폼 지원**: Python, Node.js 민팅 스크립트 제공

### 🎯 사용 사례

- **RE100 이니셔티브**: 기업의 100% 재생에너지 사용 목표 달성
- **ESG 보고**: 지속가능경영 보고서용 재생에너지 사용량 증명
- **CBAM 대응**: EU 탄소국경조정메커니즘 신고용 탄소 발자국 추적
- **탄소 크레딧 거래**: 탄소 배출권 거래소에서 활용
- **공급망 투명성**: 제품 생산 과정의 재생에너지 사용량 추적

## 🚀 빠른 시작

### 📋 필수 요구사항

- **Node.js** 16.0.0 이상
- **Python** 3.8 이상
- **Git**
- **메타마스크** 또는 기타 Web3 지갑

### 📦 설치

```bash
# 저장소 클론
git clone https://github.com/your-username/energy-certificate-nft.git
cd energy-certificate-nft

# Node.js 의존성 설치
npm install

# Python 의존성 설치 (선택사항)
cd python
pip install -r requirements.txt
cd ..
```

### 🔧 환경 설정

1. **환경 변수 설정**:
```bash
# 루트 디렉토리에 .env 파일 생성
cp .env.example .env
```

2. **.env 파일 편집**:
```env
# 블록체인 네트워크
SEPOLIA_URL=https://sepolia.infura.io/v3/YOUR_INFURA_PROJECT_ID
PRIVATE_KEY=0xYOUR_PRIVATE_KEY

# IPFS 서비스 (Pinata)
PINATA_API_KEY=YOUR_PINATA_API_KEY
PINATA_SECRET_API_KEY=YOUR_PINATA_SECRET_KEY

# API 키
ETHERSCAN_API_KEY=YOUR_ETHERSCAN_API_KEY
```

### 🔨 컴파일 및 테스트

```bash
# 스마트컨트랙트 컴파일
npm run compile

# 테스트 실행
npm test

# 커버리지 확인
npx hardhat coverage
```

## 📚 배포 가이드

### 🏠 로컬 배포

```bash
# 로컬 Hardhat 네트워크 시작
npm run node

# 다른 터미널에서 배포
npm run deploy:local
```

### 🌐 테스트넷 배포 (Sepolia)

```bash
# Sepolia 테스트넷 배포
npm run deploy:sepolia

# 컨트랙트 검증
npm run verify:sepolia CONTRACT_ADDRESS
```

### 🚀 메인넷 배포 (Polygon)

```bash
# Polygon 메인넷 배포
npm run deploy:polygon

# 컨트랙트 검증
npm run verify:polygon CONTRACT_ADDRESS
```

## 💻 사용 방법

### 🐍 Python 스크립트 사용

```python
from python.energy_nft_minter import EnergyNFTMinter
from datetime import datetime

# NFT 민터 초기화
minter = EnergyNFTMinter("python/config.json")

# 에너지 거래 데이터
energy_data = {
    "energy_amount": 1.5,  # 1.5 MWh
    "energy_type": "solar",
    "supplier": "0x742d35Cc6634C0532925a3b8D7e99B8fF4b4c4C7",
    "buyer": "0x8ba1f109551bD432803012645Hac136c903C2B3F",
    "location": "경기도 화성시 태양광발전소",
    "timestamp": datetime.now().isoformat()
}

# NFT 민팅
tx_hash = minter.mint_nft(energy_data)
print(f"🎉 NFT 민팅 완료! 트랜잭션: {tx_hash}")
```

### 🟨 Node.js API 서버 사용

```bash
# API 서버 시작
cd nodejs
npm start

# 또는 개발 모드
npm run dev
```

**API 엔드포인트**:

```bash
# 단일 NFT 민팅
curl -X POST http://localhost:3000/api/mint \
  -H "Content-Type: application/json" \
  -d '{
    "energyAmount": 1.5,
    "energyType": "solar",
    "supplier": "0x742d35Cc6634C0532925a3b8D7e99B8fF4b4c4C7",
    "buyer": "0x8ba1f109551bD432803012645Hac136c903C2B3F",
    "location": "경기도 화성시 태양광발전소"
  }'

# 토큰 정보 조회
curl http://localhost:3000/api/token/1

# 탄소 회피량 조회
curl http://localhost:3000/api/carbon-offset/0x8ba1f109551bD432803012645Hac136c903C2B3F
```

### 🎨 메타데이터 템플릿 활용

```python
from utils.ipfs_uploader import create_metadata_with_template, IPFSUploader

# 템플릿 기반 메타데이터 생성
energy_data = {
    "energy_amount": 2.0,
    "energy_type": "wind",
    "supplier": "0x...",
    "buyer": "0x...",
    "location": "제주도 풍력발전단지",
    "country": "South Korea",
    "year": 2024
}

metadata = create_metadata_with_template(energy_data)

# IPFS 업로드
uploader = IPFSUploader(service="pinata", api_key="...", secret_key="...")
ipfs_url = uploader.upload_json(metadata)
```

## 📊 스마트컨트랙트 기능

### 🏗️ 주요 함수

```solidity
// NFT 민팅
function mintEnergyNFT(
    address recipient,
    string memory tokenURI,
    uint256 energyAmount,
    address supplier,
    address buyer,
    string memory energyType,
    uint256 carbonOffset,
    string memory location
) public onlyOwner returns (uint256)

// 에너지 데이터 조회
function getEnergyData(uint256 tokenId) 
    public view returns (EnergyData memory)

// 총 탄소 회피량 계산
function getTotalCarbonOffset(address owner) 
    public view returns (uint256)

// NFT 은퇴 (크레딧 소각)
function retireNFT(uint256 tokenId) public
```

### 📈 이벤트

```solidity
// NFT 민팅 시
event EnergyNFTMinted(
    uint256 indexed tokenId,
    address indexed supplier,
    address indexed buyer,
    uint256 energyAmount,
    string energyType
);

// NFT 은퇴 시
event EnergyNFTRetired(
    uint256 indexed tokenId,
    address indexed owner
);
```

## 🧪 테스트

### 단위 테스트

```bash
# 모든 테스트 실행
npm test

# 특정 테스트 파일 실행
npx hardhat test test/EnergyCertificateNFT.test.js

# 가스 사용량 리포트
REPORT_GAS=true npm test
```

### 통합 테스트

```bash
# 전체 워크플로우 테스트
npx hardhat test test/integration.test.js

# 커버리지 리포트
npx hardhat coverage
```

## 📈 실제 사용 시나리오

### 🏢 RE100 기업 사례

```javascript
// Samsung이 재생에너지 구매 시
const samsungPurchase = {
  energyAmount: 1000, // 1 GWh
  energyType: "solar",
  supplier: "0xSolarFarmKorea",
  buyer: "0xSamsung",
  location: "전남 신안군 태양광단지"
};

// Apple이 풍력에너지 구매 시
const applePurchase = {
  energyAmount: 500, // 0.5 GWh
  energyType: "wind",
  supplier: "0xWindFarmJeju",
  buyer: "0xApple",
  location: "제주도 해상풍력단지"
};
```

### 🏭 CBAM 대응 사례

```javascript
// 수출 기업이 생산 과정에서 사용한 재생에너지 추적
const productionEnergy = [
  {
    process: "철강 제련",
    energyAmount: 2000,
    energyType: "hydro",
    carbonOffset: 48
  },
  {
    process: "자동차 조립",
    energyAmount: 800,
    energyType: "solar", 
    carbonOffset: 372
  }
];

// EU 수출 시 CBAM 신고서에 활용
const cbamReport = {
  totalEnergyUsed: 2800, // kWh
  totalCarbonAvoidance: 420, // kgCO2
  carbonIntensity: 0.15 // tCO2/MWh
};
```

## 🛠️ 개발 도구

### 📁 프로젝트 구조

```
energy-certificate-nft/
├── contracts/              # 스마트컨트랙트
│   └── EnergyCertificateNFT.sol
├── scripts/                # 배포 스크립트
│   └── deploy.js
├── test/                   # 테스트 파일
│   ├── EnergyCertificateNFT.test.js
│   └── integration.test.js
├── python/                 # Python 민팅 스크립트
│   ├── energy_nft_minter.py
│   ├── config.json
│   └── requirements.txt
├── nodejs/                 # Node.js API 서버
│   ├── energyNFTMinter.js
│   ├── package.json
│   └── .env.example
├── utils/                  # 유틸리티
│   ├── metadata_templates.json
│   └── ipfs_uploader.py
├── hardhat.config.js       # Hardhat 설정
├── package.json            # Node.js 의존성
└── README.md              # 이 파일
```

### 🔧 유용한 명령어

```bash
# 스마트컨트랙트 크기 확인
npx hardhat size-contracts

# ABI 추출
npx hardhat export-abi

# 플래튼 컨트랙트 생성 (검증용)
npx hardhat flatten contracts/EnergyCertificateNFT.sol > flattened.sol

# 가스 가격 체크
npx hardhat gas-price --network polygon
```

## 🌍 지원 네트워크

| 네트워크 | 체인 ID | RPC URL | 탐색기 |
|---------|---------|---------|---------|
| Ethereum Sepolia | 11155111 | https://sepolia.infura.io/v3/ | https://sepolia.etherscan.io |
| Polygon Mainnet | 137 | https://polygon-rpc.com/ | https://polygonscan.com |
| Polygon Mumbai | 80001 | https://rpc-mumbai.maticvigil.com/ | https://mumbai.polygonscan.com |

## 🤝 기여하기

1. **Fork** 저장소
2. **Feature 브랜치** 생성 (`git checkout -b feature/amazing-feature`)
3. **변경사항 커밋** (`git commit -m 'Add amazing feature'`)
4. **브랜치 푸시** (`git push origin feature/amazing-feature`)
5. **Pull Request** 생성

### 📝 커밋 메시지 규칙

```
feat: 새로운 기능 추가
fix: 버그 수정
docs: 문서 업데이트
style: 코드 포매팅
refactor: 코드 리팩토링
test: 테스트 추가/수정
chore: 기타 작업
```

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 🆘 지원 및 문의

- **이슈 리포트**: [GitHub Issues](https://github.com/your-username/energy-certificate-nft/issues)
- **토론**: [GitHub Discussions](https://github.com/your-username/energy-certificate-nft/discussions)
- **이메일**: energy-nft@example.com

## 🙏 감사의 말

- [OpenZeppelin](https://openzeppelin.com/) - 안전한 스마트컨트랙트 라이브러리
- [Hardhat](https://hardhat.org/) - 이더리움 개발 환경
- [Pinata](https://pinata.cloud/) - IPFS 인프라 서비스
- [RE100](https://www.there100.org/) - 재생에너지 이니셔티브

## 📊 통계

- **스마트컨트랙트**: 1개 (150+ 줄)
- **테스트 케이스**: 25+개
- **코드 커버리지**: 95%+
- **지원 언어**: Python, JavaScript
- **지원 네트워크**: 4개 이상

---

**🌱 지속 가능한 미래를 위한 블록체인 솔루션**

> "Every great dream begins with a dreamer. Always remember, you have within you the strength, the patience, and the passion to reach for the stars to change the world." - Harriet Tubman 