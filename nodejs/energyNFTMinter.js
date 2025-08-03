#!/usr/bin/env node
/**
 * 에너지 인증서 NFT 자동 민팅 서버 (Node.js + Express)
 * RE100, CBAM, 탄소거래용 NFT 생성 및 관리 API
 */

const express = require('express');
const { ethers } = require('ethers');
const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs').promises;
const path = require('path');
const dotenv = require('dotenv');

// 환경 변수 로드
dotenv.config();

class EnergyNFTMinter {
    constructor() {
        this.provider = new ethers.JsonRpcProvider(process.env.RPC_URL);
        this.wallet = new ethers.Wallet(process.env.PRIVATE_KEY, this.provider);
        this.contractAddress = process.env.CONTRACT_ADDRESS;
        this.contract = null;
        this.initContract();
    }

    async initContract() {
        try {
            // ABI 파일 로드
            const abiPath = path.join(__dirname, '../artifacts/contracts/EnergyCertificateNFT.sol/EnergyCertificateNFT.json');
            const contractJson = JSON.parse(await fs.readFile(abiPath, 'utf8'));
            
            this.contract = new ethers.Contract(
                this.contractAddress,
                contractJson.abi,
                this.wallet
            );
            
            console.log('✅ 스마트컨트랙트 연결 완료');
        } catch (error) {
            console.error('❌ 컨트랙트 초기화 실패:', error);
        }
    }

    /**
     * 에너지 타입별 이미지 URL 반환
     */
    getEnergyTypeImage(energyType) {
        const imageMapping = {
            'solar': 'ipfs://QmSolarPanelIcon/solar.png',
            'wind': 'ipfs://QmWindTurbineIcon/wind.png',
            'hydro': 'ipfs://QmHydroIcon/hydro.png',
            'biomass': 'ipfs://QmBiomassIcon/biomass.png'
        };
        return imageMapping[energyType] || 'ipfs://QmDefaultEnergyIcon/default.png';
    }

    /**
     * 탄소 회피량 계산
     */
    calculateCarbonOffset(energyAmount, energyType) {
        const carbonFactors = {
            'solar': 0.466,
            'wind': 0.011,
            'hydro': 0.024,
            'biomass': 0.18
        };
        return energyAmount * (carbonFactors[energyType] || 0.4);
    }

    /**
     * NFT 메타데이터 생성
     */
    generateMetadata(energyData) {
        const carbonOffset = this.calculateCarbonOffset(
            energyData.energyAmount, 
            energyData.energyType
        );

        return {
            name: `RE100 전력 NFT #${energyData.tokenId || 'TBD'}`,
            description: `${energyData.energyAmount}MWh ${energyData.energyType} 전력 거래 인증서`,
            image: this.getEnergyTypeImage(energyData.energyType),
            external_url: `https://energy-nft.com/token/${energyData.tokenId || ''}`,
            attributes: [
                {
                    trait_type: "전력량 (MWh)",
                    value: energyData.energyAmount,
                    display_type: "number"
                },
                {
                    trait_type: "에너지 타입",
                    value: energyData.energyType
                },
                {
                    trait_type: "거래일시",
                    value: energyData.timestamp || new Date().toISOString()
                },
                {
                    trait_type: "공급자",
                    value: energyData.supplier
                },
                {
                    trait_type: "수요자",
                    value: energyData.buyer
                },
                {
                    trait_type: "발전소 위치",
                    value: energyData.location
                },
                {
                    trait_type: "탄소 회피량 (tCO₂)",
                    value: Math.round(carbonOffset * 1000) / 1000,
                    display_type: "number"
                },
                {
                    trait_type: "RE100 적합성",
                    value: "인증됨"
                },
                {
                    trait_type: "CBAM 대응",
                    value: "적합"
                }
            ],
            properties: {
                category: "Energy Certificate",
                subcategory: energyData.energyType.charAt(0).toUpperCase() + energyData.energyType.slice(1),
                is_renewable: true,
                certification_standard: "RE100",
                carbon_offset_tco2: carbonOffset,
                energy_amount_mwh: energyData.energyAmount
            }
        };
    }

    /**
     * IPFS에 메타데이터 업로드 (Pinata 사용)
     */
    async uploadToIPFS(metadata) {
        try {
            const formData = new FormData();
            const jsonBuffer = Buffer.from(JSON.stringify(metadata, null, 2));
            
            formData.append('file', jsonBuffer, {
                filename: `metadata_${Date.now()}.json`,
                contentType: 'application/json'
            });

            const response = await axios.post(
                'https://api.pinata.cloud/pinning/pinFileToIPFS',
                formData,
                {
                    headers: {
                        ...formData.getHeaders(),
                        'pinata_api_key': process.env.PINATA_API_KEY,
                        'pinata_secret_api_key': process.env.PINATA_SECRET_KEY
                    }
                }
            );

            const ipfsHash = response.data.IpfsHash;
            const ipfsUrl = `ipfs://${ipfsHash}`;
            
            console.log(`✅ IPFS 업로드 완료: ${ipfsUrl}`);
            return ipfsUrl;

        } catch (error) {
            console.error('❌ IPFS 업로드 실패:', error.message);
            throw error;
        }
    }

    /**
     * 에너지 NFT 민팅
     */
    async mintEnergyNFT(energyData) {
        try {
            console.log('🚀 NFT 민팅 시작...');

            // 1. 메타데이터 생성
            const metadata = this.generateMetadata(energyData);
            console.log('📄 메타데이터 생성 완료');

            // 2. IPFS 업로드
            const tokenURI = await this.uploadToIPFS(metadata);

            // 3. 탄소 회피량 계산 (정수로 변환)
            const carbonOffset = Math.floor(
                this.calculateCarbonOffset(energyData.energyAmount, energyData.energyType) * 1000
            );

            // 4. 에너지량을 kWh로 변환
            const energyAmountKWh = Math.floor(energyData.energyAmount * 1000);

            // 5. 스마트컨트랙트 함수 호출
            const tx = await this.contract.mintEnergyNFT(
                energyData.buyer,           // recipient
                tokenURI,                   // tokenURI
                energyAmountKWh,           // energyAmount (kWh)
                energyData.supplier,        // supplier
                energyData.buyer,          // buyer
                energyData.energyType,     // energyType
                carbonOffset,              // carbonOffset
                energyData.location,       // location
                {
                    gasLimit: 500000,
                    gasPrice: ethers.parseUnits('10', 'gwei')
                }
            );

            console.log(`✅ 민팅 트랜잭션 전송: ${tx.hash}`);

            // 6. 트랜잭션 확인 대기
            const receipt = await tx.wait();
            
            if (receipt.status === 1) {
                console.log(`🎉 NFT 민팅 성공! Gas 사용량: ${receipt.gasUsed}`);
                
                // 이벤트에서 토큰 ID 추출
                const event = receipt.logs.find(log => {
                    try {
                        return this.contract.interface.parseLog(log).name === 'EnergyNFTMinted';
                    } catch {
                        return false;
                    }
                });

                let tokenId = null;
                if (event) {
                    const parsedEvent = this.contract.interface.parseLog(event);
                    tokenId = parsedEvent.args.tokenId.toString();
                }

                return {
                    success: true,
                    txHash: tx.hash,
                    tokenId: tokenId,
                    gasUsed: receipt.gasUsed.toString(),
                    tokenURI: tokenURI,
                    metadata: metadata
                };
            } else {
                throw new Error('트랜잭션 실패');
            }

        } catch (error) {
            console.error('❌ NFT 민팅 실패:', error);
            return {
                success: false,
                error: error.message
            };
        }
    }

    /**
     * 배치 민팅
     */
    async batchMint(energyDataList) {
        const results = [];
        
        for (let i = 0; i < energyDataList.length; i++) {
            console.log(`📦 배치 민팅 진행 중... (${i + 1}/${energyDataList.length})`);
            
            const result = await this.mintEnergyNFT(energyDataList[i]);
            results.push({
                index: i,
                data: energyDataList[i],
                result: result
            });

            // API 레이트 리미트 방지
            if (i < energyDataList.length - 1) {
                await new Promise(resolve => setTimeout(resolve, 2000));
            }
        }

        return results;
    }

    /**
     * 토큰 정보 조회
     */
    async getTokenInfo(tokenId) {
        try {
            const energyData = await this.contract.getEnergyData(tokenId);
            const tokenURI = await this.contract.tokenURI(tokenId);
            const owner = await this.contract.ownerOf(tokenId);

            return {
                tokenId: tokenId,
                owner: owner,
                tokenURI: tokenURI,
                energyData: {
                    energyAmount: energyData.energyAmount.toString(),
                    timestamp: new Date(Number(energyData.timestamp) * 1000).toISOString(),
                    supplier: energyData.supplier,
                    buyer: energyData.buyer,
                    energyType: energyData.energyType,
                    carbonOffset: energyData.carbonOffset.toString(),
                    location: energyData.location,
                    isRetired: energyData.isRetired
                }
            };
        } catch (error) {
            throw new Error(`토큰 정보 조회 실패: ${error.message}`);
        }
    }

    /**
     * 총 탄소 회피량 조회
     */
    async getTotalCarbonOffset(ownerAddress) {
        try {
            const totalOffset = await this.contract.getTotalCarbonOffset(ownerAddress);
            return (Number(totalOffset) / 1000).toString(); // tCO2 단위로 변환
        } catch (error) {
            throw new Error(`탄소 회피량 조회 실패: ${error.message}`);
        }
    }
}

// Express 서버 설정
const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());
app.use(express.static('public'));

// CORS 미들웨어
app.use((req, res, next) => {
    res.header('Access-Control-Allow-Origin', '*');
    res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept');
    res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE');
    next();
});

// NFT 민터 인스턴스
const minter = new EnergyNFTMinter();

// API 엔드포인트
app.get('/', (req, res) => {
    res.json({
        message: '🌱 에너지 인증서 NFT 민팅 API',
        version: '1.0.0',
        endpoints: {
            mint: 'POST /api/mint',
            batchMint: 'POST /api/batch-mint',
            tokenInfo: 'GET /api/token/:tokenId',
            carbonOffset: 'GET /api/carbon-offset/:address'
        }
    });
});

// 단일 NFT 민팅
app.post('/api/mint', async (req, res) => {
    try {
        const energyData = req.body;
        
        // 필수 필드 검증
        const requiredFields = ['energyAmount', 'energyType', 'supplier', 'buyer', 'location'];
        for (const field of requiredFields) {
            if (!energyData[field]) {
                return res.status(400).json({
                    success: false,
                    error: `필수 필드 누락: ${field}`
                });
            }
        }

        const result = await minter.mintEnergyNFT(energyData);
        res.json(result);

    } catch (error) {
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

// 배치 민팅
app.post('/api/batch-mint', async (req, res) => {
    try {
        const { energyDataList } = req.body;
        
        if (!Array.isArray(energyDataList) || energyDataList.length === 0) {
            return res.status(400).json({
                success: false,
                error: 'energyDataList는 비어있지 않은 배열이어야 합니다.'
            });
        }

        const results = await minter.batchMint(energyDataList);
        res.json({
            success: true,
            results: results
        });

    } catch (error) {
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

// 토큰 정보 조회
app.get('/api/token/:tokenId', async (req, res) => {
    try {
        const tokenId = req.params.tokenId;
        const tokenInfo = await minter.getTokenInfo(tokenId);
        res.json({
            success: true,
            data: tokenInfo
        });

    } catch (error) {
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

// 탄소 회피량 조회
app.get('/api/carbon-offset/:address', async (req, res) => {
    try {
        const address = req.params.address;
        const totalOffset = await minter.getTotalCarbonOffset(address);
        res.json({
            success: true,
            address: address,
            totalCarbonOffset: totalOffset,
            unit: 'tCO₂'
        });

    } catch (error) {
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

// 서버 시작
app.listen(PORT, () => {
    console.log(`🚀 에너지 NFT 민팅 서버가 http://localhost:${PORT}에서 실행 중입니다.`);
    console.log(`📡 네트워크: ${process.env.NETWORK || 'sepolia'}`);
    console.log(`📍 컨트랙트: ${process.env.CONTRACT_ADDRESS}`);
});

module.exports = { EnergyNFTMinter, app };