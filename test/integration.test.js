const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("통합 테스트: 전체 민팅 워크플로우", function () {
    let energyNFT;
    let owner;
    let supplier;
    let buyer;
    let addrs;

    // 실제 에너지 거래 시나리오 데이터
    const energyTradeScenarios = [
        {
            name: "태양광 발전소 거래",
            energyAmount: 1500, // 1.5 MWh
            energyType: "solar",
            location: "경기도 화성시 태양광발전소",
            carbonOffset: 699, // 1.5 * 0.466 * 1000
            tokenURI: "ipfs://QmSolar123"
        },
        {
            name: "풍력 발전소 거래",
            energyAmount: 5000, // 5 MWh
            energyType: "wind",
            location: "제주도 풍력발전단지",
            carbonOffset: 55, // 5 * 0.011 * 1000
            tokenURI: "ipfs://QmWind456"
        },
        {
            name: "수력 발전소 거래",
            energyAmount: 2000, // 2 MWh
            energyType: "hydro",
            location: "충청북도 수력발전소",
            carbonOffset: 48, // 2 * 0.024 * 1000
            tokenURI: "ipfs://QmHydro789"
        }
    ];

    beforeEach(async function () {
        [owner, supplier, buyer, ...addrs] = await ethers.getSigners();

        const EnergyCertificateNFT = await ethers.getContractFactory("EnergyCertificateNFT");
        energyNFT = await EnergyCertificateNFT.deploy();
        await energyNFT.waitForDeployment();
    });

    describe("RE100 기업의 전력 구매 시나리오", function () {
        it("다양한 재생에너지 NFT를 순차적으로 민팅해야 함", async function () {
            let totalCarbonOffset = 0;
            const mintedTokens = [];

            for (let i = 0; i < energyTradeScenarios.length; i++) {
                const scenario = energyTradeScenarios[i];
                
                // NFT 민팅
                const tx = await energyNFT.mintEnergyNFT(
                    buyer.address,
                    scenario.tokenURI,
                    scenario.energyAmount,
                    supplier.address,
                    buyer.address,
                    scenario.energyType,
                    scenario.carbonOffset,
                    scenario.location
                );

                const tokenId = i + 1;
                mintedTokens.push(tokenId);

                // 이벤트 확인
                await expect(tx)
                    .to.emit(energyNFT, "EnergyNFTMinted")
                    .withArgs(tokenId, supplier.address, buyer.address, scenario.energyAmount, scenario.energyType);

                // 토큰 소유권 확인
                expect(await energyNFT.ownerOf(tokenId)).to.equal(buyer.address);

                // 에너지 데이터 확인
                const energyData = await energyNFT.getEnergyData(tokenId);
                expect(energyData.energyAmount).to.equal(scenario.energyAmount);
                expect(energyData.energyType).to.equal(scenario.energyType);
                expect(energyData.carbonOffset).to.equal(scenario.carbonOffset);
                expect(energyData.location).to.equal(scenario.location);
                expect(energyData.isRetired).to.equal(false);

                totalCarbonOffset += scenario.carbonOffset;
            }

            // 총 탄소 회피량 확인
            const calculatedOffset = await energyNFT.getTotalCarbonOffset(buyer.address);
            expect(calculatedOffset).to.equal(totalCarbonOffset);

            // 총 토큰 수 확인
            expect(await energyNFT.balanceOf(buyer.address)).to.equal(energyTradeScenarios.length);

            console.log(`✅ ${energyTradeScenarios.length}개의 에너지 NFT 민팅 완료`);
            console.log(`🌱 총 탄소 회피량: ${totalCarbonOffset / 1000} tCO₂`);
        });

        it("NFT 은퇴를 통한 탄소 크레딧 사용", async function () {
            // 모든 시나리오의 NFT 민팅
            for (let i = 0; i < energyTradeScenarios.length; i++) {
                const scenario = energyTradeScenarios[i];
                await energyNFT.mintEnergyNFT(
                    buyer.address,
                    scenario.tokenURI,
                    scenario.energyAmount,
                    supplier.address,
                    buyer.address,
                    scenario.energyType,
                    scenario.carbonOffset,
                    scenario.location
                );
            }

            // 첫 번째 NFT 은퇴 (태양광)
            const tokenIdToRetire = 1;
            const retireTx = await energyNFT.connect(buyer).retireNFT(tokenIdToRetire);
            
            await expect(retireTx)
                .to.emit(energyNFT, "EnergyNFTRetired")
                .withArgs(tokenIdToRetire, buyer.address);

            // 은퇴 상태 확인
            const energyDataAfterRetire = await energyNFT.getEnergyData(tokenIdToRetire);
            expect(energyDataAfterRetire.isRetired).to.equal(true);

            // 은퇴 후 탄소 회피량 재계산 (은퇴한 NFT 제외)
            const expectedOffsetAfterRetire = energyTradeScenarios
                .slice(1)
                .reduce((sum, scenario) => sum + scenario.carbonOffset, 0);
            
            const actualOffsetAfterRetire = await energyNFT.getTotalCarbonOffset(buyer.address);
            expect(actualOffsetAfterRetire).to.equal(expectedOffsetAfterRetire);

            console.log(`♻️ NFT #${tokenIdToRetire} 은퇴 완료`);
            console.log(`🌱 은퇴 후 남은 탄소 회피량: ${actualOffsetAfterRetire / 1000} tCO₂`);
        });
    });

    describe("배치 처리 시나리오", function () {
        it("대량 거래 데이터 처리", async function () {
            const batchSize = 10;
            const baseEnergyAmount = 1000;
            
            // 대량 NFT 민팅
            for (let i = 0; i < batchSize; i++) {
                await energyNFT.mintEnergyNFT(
                    buyer.address,
                    `ipfs://QmBatch${i}`,
                    baseEnergyAmount + (i * 100),
                    supplier.address,
                    buyer.address,
                    "solar",
                    Math.floor((baseEnergyAmount + (i * 100)) * 0.466),
                    `Location ${i}`
                );
            }

            // 배치 처리 결과 확인
            expect(await energyNFT.balanceOf(buyer.address)).to.equal(batchSize);
            
            // 마지막 토큰 확인
            const lastTokenData = await energyNFT.getEnergyData(batchSize);
            expect(lastTokenData.energyAmount).to.equal(baseEnergyAmount + ((batchSize - 1) * 100));

            console.log(`📦 배치 처리 완료: ${batchSize}개 NFT`);
        });
    });

    describe("실제 사용 사례: ESG 보고", function () {
        it("연간 재생에너지 사용량 및 탄소 감축량 추적", async function () {
            const monthlyData = [
                { month: "2024-01", energyAmount: 1200, carbonOffset: 559 },
                { month: "2024-02", energyAmount: 1100, carbonOffset: 512 },
                { month: "2024-03", energyAmount: 1300, carbonOffset: 605 },
            ];

            const annualReports = [];

            for (let i = 0; i < monthlyData.length; i++) {
                const data = monthlyData[i];
                
                await energyNFT.mintEnergyNFT(
                    buyer.address,
                    `ipfs://QmMonthly${i}`,
                    data.energyAmount,
                    supplier.address,
                    buyer.address,
                    "solar",
                    data.carbonOffset,
                    `Monthly Report ${data.month}`
                );

                const tokenId = i + 1;
                const energyData = await energyNFT.getEnergyData(tokenId);
                
                annualReports.push({
                    tokenId: tokenId,
                    month: data.month,
                    energyAmount: energyData.energyAmount.toString(),
                    carbonOffset: energyData.carbonOffset.toString(),
                    timestamp: energyData.timestamp.toString()
                });
            }

            // 연간 총 탄소 회피량
            const totalAnnualOffset = await energyNFT.getTotalCarbonOffset(buyer.address);
            const expectedTotal = monthlyData.reduce((sum, data) => sum + data.carbonOffset, 0);
            
            expect(totalAnnualOffset).to.equal(expectedTotal);

            console.log("📊 연간 ESG 보고서:");
            console.log(`📋 총 NFT 수: ${annualReports.length}`);
            console.log(`⚡ 총 재생에너지 사용량: ${monthlyData.reduce((sum, data) => sum + data.energyAmount, 0) / 1000} MWh`);
            console.log(`🌱 총 탄소 감축량: ${totalAnnualOffset / 1000} tCO₂`);
        });
    });

    describe("CBAM (탄소국경조정메커니즘) 대응", function () {
        it("수출용 제품의 탄소 발자국 추적", async function () {
            // 제조업체가 생산 과정에서 사용한 재생에너지
            const productionEnergyData = [
                {
                    process: "원자재 가공",
                    energyAmount: 800,
                    energyType: "solar",
                    carbonOffset: 372
                },
                {
                    process: "제품 조립",
                    energyAmount: 600,
                    energyType: "wind",
                    carbonOffset: 6
                },
                {
                    process: "품질 검사",
                    energyAmount: 200,
                    energyType: "hydro",
                    carbonOffset: 4
                }
            ];

            const productionNFTs = [];

            for (let i = 0; i < productionEnergyData.length; i++) {
                const data = productionEnergyData[i];
                
                await energyNFT.mintEnergyNFT(
                    buyer.address,
                    `ipfs://QmProduction${i}`,
                    data.energyAmount,
                    supplier.address,
                    buyer.address,
                    data.energyType,
                    data.carbonOffset,
                    `Production: ${data.process}`
                );

                productionNFTs.push(i + 1);
            }

            // CBAM 신고용 총 탄소 회피량 계산
            const totalCarbonAvoidance = await energyNFT.getTotalCarbonOffset(buyer.address);
            const totalEnergyUsed = productionEnergyData.reduce((sum, data) => sum + data.energyAmount, 0);

            // 탄소 집약도 계산 (tCO₂/MWh)
            const carbonIntensity = (totalCarbonAvoidance / 1000) / (totalEnergyUsed / 1000);

            expect(totalCarbonAvoidance).to.be.greaterThan(0);
            expect(productionNFTs.length).to.equal(3);

            console.log("🏭 CBAM 대응 보고서:");
            console.log(`🔧 생산 공정 수: ${productionEnergyData.length}`);
            console.log(`⚡ 총 에너지 사용량: ${totalEnergyUsed / 1000} MWh`);
            console.log(`🌱 총 탄소 회피량: ${totalCarbonAvoidance / 1000} tCO₂`);
            console.log(`📊 탄소 집약도: ${carbonIntensity.toFixed(3)} tCO₂/MWh`);
        });
    });

    describe("Error 처리 및 Edge Cases", function () {
        it("가스 한도 초과 시나리오", async function () {
            // 매우 긴 문자열로 가스 한도 테스트
            const longLocation = "A".repeat(1000);
            
            await expect(energyNFT.mintEnergyNFT(
                buyer.address,
                "ipfs://QmTest",
                1000,
                supplier.address,
                buyer.address,
                "solar",
                466,
                longLocation
            )).to.not.be.reverted; // 정상적으로 처리되어야 함
        });

        it("잘못된 주소 처리", async function () {
            // 영 주소로 민팅 시도
            await expect(energyNFT.mintEnergyNFT(
                ethers.ZeroAddress,
                "ipfs://QmTest",
                1000,
                supplier.address,
                buyer.address,
                "solar",
                466,
                "Test Location"
            )).to.be.revertedWith("ERC721: mint to the zero address");
        });
    });
});