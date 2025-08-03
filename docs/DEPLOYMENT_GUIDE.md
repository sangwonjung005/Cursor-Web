# 🚀 배포 가이드

Energy Certificate NFT 프로젝트의 완전한 배포 가이드입니다.

## 📋 목차

1. [사전 준비](#사전-준비)
2. [로컬 환경 배포](#로컬-환경-배포)
3. [테스트넷 배포](#테스트넷-배포)
4. [메인넷 배포](#메인넷-배포)
5. [Python 스크립트 설정](#python-스크립트-설정)
6. [Node.js API 서버 배포](#nodejs-api-서버-배포)
7. [모니터링 및 유지보수](#모니터링-및-유지보수)

## 🛠️ 사전 준비

### 필수 계정 및 서비스

#### 1. **Infura 계정** (RPC 노드 제공)
```bash
# 1. https://infura.io 회원가입
# 2. 새 프로젝트 생성
# 3. Project ID 복사
PROJECT_ID=your_project_id_here
```

#### 2. **Pinata 계정** (IPFS 서비스)
```bash
# 1. https://pinata.cloud 회원가입
# 2. API Keys 생성
# 3. API Key & Secret 복사
PINATA_API_KEY=your_api_key_here
PINATA_SECRET_KEY=your_secret_key_here
```

#### 3. **Etherscan API Key** (컨트랙트 검증)
```bash
# 1. https://etherscan.io/apis 계정 생성
# 2. API Key 생성
ETHERSCAN_API_KEY=your_api_key_here
```

#### 4. **MetaMask 지갑 설정**
```bash
# 개인 키 추출 (매우 중요한 보안 정보!)
# MetaMask > 계정 세부 정보 > 개인 키 내보내기
PRIVATE_KEY=0x1234567890abcdef...
```

### 🔑 환경 변수 설정

`.env` 파일 생성:
```env
# 네트워크 설정
SEPOLIA_URL=https://sepolia.infura.io/v3/YOUR_INFURA_PROJECT_ID
POLYGON_URL=https://polygon-mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID
MUMBAI_URL=https://polygon-mumbai.infura.io/v3/YOUR_INFURA_PROJECT_ID

# 개인 키 (0x 포함)
PRIVATE_KEY=0xYOUR_PRIVATE_KEY

# API 키들
ETHERSCAN_API_KEY=YOUR_ETHERSCAN_API_KEY
POLYGONSCAN_API_KEY=YOUR_POLYGONSCAN_API_KEY
PINATA_API_KEY=YOUR_PINATA_API_KEY
PINATA_SECRET_API_KEY=YOUR_PINATA_SECRET_KEY

# 가스 설정
REPORT_GAS=true
COINMARKETCAP_API_KEY=YOUR_COINMARKETCAP_API_KEY
```

## 🏠 로컬 환경 배포

### 1. Hardhat 로컬 네트워크 시작

```bash
# 터미널 1: 로컬 블록체인 시작
npm run node

# 출력 예시:
# Started HTTP and WebSocket JSON-RPC server at http://127.0.0.1:8545/
# 
# Accounts
# ========
# Account #0: 0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266 (10000 ETH)
# Private Key: 0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80
```

### 2. 스마트컨트랙트 배포

```bash
# 터미널 2: 컨트랙트 배포
npm run deploy:local

# 출력 예시:
# 🚀 에너지 인증서 NFT 배포 시작...
# 📦 컨트랙트 배포 중...
# ✅ EnergyCertificateNFT 배포 완료!
# 📍 컨트랙트 주소: 0x5FbDB2315678afecb367f032d93F642f64180aa3
# 🌐 네트워크: hardhat
# 🆔 체인 ID: 1337
```

### 3. 로컬 테스트

```bash
# 컨트랙트 테스트
npm test

# 커버리지 확인
npx hardhat coverage
```

## 🌐 테스트넷 배포

### 1. Sepolia 테스트넷

#### 테스트 ETH 받기
```bash
# Sepolia 파우셋 사이트들:
# https://sepoliafaucet.com/
# https://faucet.quicknode.com/ethereum/sepolia
# https://www.alchemy.com/faucets/ethereum-sepolia
```

#### 배포 실행
```bash
# Sepolia 테스트넷 배포
npm run deploy:sepolia

# 출력 예시:
# 🚀 에너지 인증서 NFT 배포 시작...
# 📦 컨트랙트 배포 중...
# ✅ EnergyCertificateNFT 배포 완료!
# 📍 컨트랙트 주소: 0x742d35Cc6634C0532925a3b8D7e99B8fF4b4c4C7
# 🌐 네트워크: sepolia
# 🆔 체인 ID: 11155111
# 
# 🔍 Etherscan 검증 명령어:
# npx hardhat verify --network sepolia 0x742d35Cc6634C0532925a3b8D7e99B8fF4b4c4C7
```

#### 컨트랙트 검증
```bash
# Etherscan에서 소스코드 검증
npx hardhat verify --network sepolia 0x742d35Cc6634C0532925a3b8D7e99B8fF4b4c4C7

# 성공 시:
# Successfully submitted source code for contract
# contracts/EnergyCertificateNFT.sol:EnergyCertificateNFT at 0x742d35...
# for verification on the block explorer. Waiting for verification result...
# 
# Successfully verified contract EnergyCertificateNFT on Etherscan.
# https://sepolia.etherscan.io/address/0x742d35Cc6634C0532925a3b8D7e99B8fF4b4c4C7#code
```

### 2. Polygon Mumbai 테스트넷

#### 테스트 MATIC 받기
```bash
# Mumbai 파우셋:
# https://faucet.polygon.technology/
# https://mumbaifaucet.com/
```

#### 배포 실행
```bash
npm run deploy:mumbai
```

## 🚀 메인넷 배포

⚠️ **주의**: 메인넷 배포는 실제 비용이 발생합니다!

### 1. Polygon 메인넷

#### 사전 준비
```bash
# 1. 충분한 MATIC 보유 확인 (최소 0.1 MATIC)
# 2. 가스 가격 확인
npx hardhat gas-price --network polygon

# 3. 배포 비용 예측
npx hardhat estimate-gas --network polygon scripts/deploy.js
```

#### 배포 실행
```bash
# Polygon 메인넷 배포
npm run deploy:polygon

# 가스 한도 수동 설정 (필요시)
npx hardhat run scripts/deploy.js --network polygon --gas-limit 3000000
```

#### 배포 후 검증
```bash
# PolygonScan 검증
npm run verify:polygon CONTRACT_ADDRESS

# 배포 정보 저장
echo "Contract Address: CONTRACT_ADDRESS" >> deployment.log
echo "Network: Polygon Mainnet" >> deployment.log
echo "Date: $(date)" >> deployment.log
```

## 🐍 Python 스크립트 설정

### 1. Python 환경 설정

```bash
# Python 가상환경 생성
python -m venv venv

# 가상환경 활성화
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 의존성 설치
cd python
pip install -r requirements.txt
```

### 2. 설정 파일 구성

`python/config.json` 편집:
```json
{
  "network": "polygon",
  "rpc_url": "https://polygon-rpc.com/",
  "contract_address": "0xYOUR_DEPLOYED_CONTRACT_ADDRESS",
  "contract_abi_path": "../artifacts/contracts/EnergyCertificateNFT.sol/EnergyCertificateNFT.json",
  "private_key": "0xYOUR_PRIVATE_KEY",
  "pinata_api_key": "YOUR_PINATA_API_KEY",
  "pinata_secret_key": "YOUR_PINATA_SECRET_KEY",
  "gas_price_gwei": 30,
  "gas_limit": 500000
}
```

### 3. 민팅 테스트

```bash
# 테스트 민팅 실행
python energy_nft_minter.py

# 성공 시 출력:
# ✅ 설정 파일 로드 완료
# ✅ polygon 네트워크 연결 완료
# ✅ 스마트컨트랙트 연결 완료
# 🚀 NFT 민팅 시작...
# 📄 메타데이터 생성 완료
# ✅ IPFS 업로드 완료: ipfs://QmXxx...
# ✅ 민팅 트랜잭션 전송 완료: 0xabc123...
# 🎉 NFT 민팅 성공! Gas 사용량: 250000
```

## 🟨 Node.js API 서버 배포

### 1. 로컬 개발 서버

```bash
cd nodejs

# 환경 변수 설정
cp .env.example .env
# .env 파일 편집

# 의존성 설치
npm install

# 개발 서버 시작
npm run dev

# 서버 실행 확인:
# 🚀 에너지 NFT 민팅 서버가 http://localhost:3000에서 실행 중입니다.
# 📡 네트워크: polygon
# 📍 컨트랙트: 0xYOUR_CONTRACT_ADDRESS
```

### 2. API 테스트

```bash
# 서버 상태 확인
curl http://localhost:3000/

# NFT 민팅 테스트
curl -X POST http://localhost:3000/api/mint \
  -H "Content-Type: application/json" \
  -d '{
    "energyAmount": 1.5,
    "energyType": "solar",
    "supplier": "0x742d35Cc6634C0532925a3b8D7e99B8fF4b4c4C7",
    "buyer": "0x8ba1f109551bD432803012645Hac136c903C2B3F",
    "location": "경기도 화성시 태양광발전소"
  }'
```

### 3. 프로덕션 배포 (PM2 사용)

```bash
# PM2 설치
npm install -g pm2

# 프로덕션 시작
NODE_ENV=production pm2 start energyNFTMinter.js --name "energy-nft-api"

# 상태 확인
pm2 status

# 로그 확인
pm2 logs energy-nft-api

# 자동 재시작 설정
pm2 startup
pm2 save
```

### 4. Nginx 리버스 프록시 설정

```nginx
# /etc/nginx/sites-available/energy-nft-api
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
}
```

## 📊 모니터링 및 유지보수

### 1. 가스 가격 모니터링

```bash
# 현재 가스 가격 확인
npx hardhat gas-price --network polygon

# 가스 트래커 스크립트 작성
cat > gas-monitor.js << 'EOF'
const { ethers } = require('ethers');

async function checkGasPrice() {
    const provider = new ethers.JsonRpcProvider('https://polygon-rpc.com/');
    const gasPrice = await provider.getGasPrice();
    console.log(`Current gas price: ${ethers.formatUnits(gasPrice, 'gwei')} gwei`);
}

setInterval(checkGasPrice, 60000); // 1분마다 체크
EOF

node gas-monitor.js
```

### 2. 컨트랙트 상태 모니터링

```javascript
// contract-monitor.js
const { ethers } = require('ethers');

async function monitorContract() {
    const provider = new ethers.JsonRpcProvider(process.env.POLYGON_URL);
    const contract = new ethers.Contract(
        process.env.CONTRACT_ADDRESS,
        contractABI,
        provider
    );

    // 총 발행량 확인
    const totalSupply = await contract.totalSupply();
    console.log(`Total NFTs minted: ${totalSupply}`);

    // 소유자 확인
    const owner = await contract.owner();
    console.log(`Contract owner: ${owner}`);

    // 일시정지 상태 확인
    const paused = await contract.paused();
    console.log(`Contract paused: ${paused}`);
}

setInterval(monitorContract, 300000); // 5분마다 체크
```

### 3. 자동 백업 스크립트

```bash
#!/bin/bash
# backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="./backups/$DATE"

# 백업 디렉토리 생성
mkdir -p $BACKUP_DIR

# 설정 파일 백업
cp .env $BACKUP_DIR/
cp python/config.json $BACKUP_DIR/
cp nodejs/.env $BACKUP_DIR/node_env

# 컨트랙트 정보 백업
echo "Contract Address: $CONTRACT_ADDRESS" > $BACKUP_DIR/contract_info.txt
echo "Network: polygon" >> $BACKUP_DIR/contract_info.txt
echo "Backup Date: $(date)" >> $BACKUP_DIR/contract_info.txt

# ABI 백업
cp artifacts/contracts/EnergyCertificateNFT.sol/EnergyCertificateNFT.json $BACKUP_DIR/

echo "Backup completed: $BACKUP_DIR"
```

### 4. 로그 설정

```javascript
// logger.js
const winston = require('winston');

const logger = winston.createLogger({
    level: 'info',
    format: winston.format.combine(
        winston.format.timestamp(),
        winston.format.errors({ stack: true }),
        winston.format.json()
    ),
    defaultMeta: { service: 'energy-nft' },
    transports: [
        new winston.transports.File({ filename: 'error.log', level: 'error' }),
        new winston.transports.File({ filename: 'combined.log' }),
        new winston.transports.Console({
            format: winston.format.simple()
        })
    ]
});

module.exports = logger;
```

## 🚨 문제 해결

### 일반적인 배포 오류

#### 1. **가스 부족 오류**
```bash
Error: insufficient funds for gas * price + value

해결책:
1. 지갑에 충분한 ETH/MATIC 확보
2. 가스 가격 조정: gasPrice: ethers.parseUnits('20', 'gwei')
```

#### 2. **Nonce 오류**
```bash
Error: nonce too low

해결책:
1. MetaMask 설정 > 고급 > 계정 재설정
2. 수동 nonce 설정: nonce: await provider.getTransactionCount(address)
```

#### 3. **네트워크 연결 오류**
```bash
Error: could not detect network

해결책:
1. RPC URL 확인
2. Infura 프로젝트 ID 확인
3. 네트워크 상태 확인: https://status.infura.io/
```

### 컨트랙트 검증 실패

```bash
# 플래튼 컨트랙트 생성 후 수동 검증
npx hardhat flatten contracts/EnergyCertificateNFT.sol > flattened.sol

# Etherscan에서 수동 업로드:
# 1. https://sepolia.etherscan.io/verifyContract
# 2. flattened.sol 내용 복사 붙여넣기
# 3. 컴파일러 버전: 0.8.19
# 4. Optimization: Yes, 200 runs
```

## ✅ 배포 체크리스트

### 테스트넷 배포
- [ ] 환경 변수 설정 완료
- [ ] 테스트 토큰 확보
- [ ] 컨트랙트 컴파일 성공
- [ ] 테스트 케이스 통과
- [ ] 컨트랙트 배포 성공
- [ ] Etherscan 검증 완료
- [ ] Python 스크립트 테스트
- [ ] Node.js API 테스트

### 메인넷 배포
- [ ] 테스트넷 배포 완료
- [ ] 보안 감사 완료
- [ ] 충분한 가스비 준비
- [ ] 백업 스크립트 설정
- [ ] 모니터링 도구 설정
- [ ] 긴급 대응 계획 수립
- [ ] 팀 내 검토 완료
- [ ] 컨트랙트 배포 및 검증
- [ ] 프로덕션 테스트 완료

---

이 가이드를 따라 성공적으로 배포하시기 바랍니다! 문제가 발생하면 GitHub Issues를 통해 문의해 주세요.