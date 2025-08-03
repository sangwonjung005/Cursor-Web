const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("EnergyCertificateNFT", function () {
    let energyNFT;
    let owner;
    let supplier;
    let buyer;
    let recipient;
    let addrs;

    beforeEach(async function () {
        // 계정 설정
        [owner, supplier, buyer, recipient, ...addrs] = await ethers.getSigners();

        // 컨트랙트 배포
        const EnergyCertificateNFT = await ethers.getContractFactory("EnergyCertificateNFT");
        energyNFT = await EnergyCertificateNFT.deploy();
        await energyNFT.waitForDeployment();
    });

    describe("배포", function () {
        it("올바른 이름과 심볼로 배포되어야 함", async function () {
            expect(await energyNFT.name()).to.equal("EnergyCertificateNFT");
            expect(await energyNFT.symbol()).to.equal("ECN");
        });

        it("소유자가 올바르게 설정되어야 함", async function () {
            expect(await energyNFT.owner()).to.equal(owner.address);
        });

        it("초기 토큰 카운터가 1이어야 함", async function () {
            // 첫 번째 토큰 ID는 1이어야 함
            const tokenURI = "ipfs://QmTest123";
            await energyNFT.mintEnergyNFT(
                recipient.address,
                tokenURI,
                1000, // 1 MWh
                supplier.address,
                buyer.address,
                "solar",
                466, // 0.466 tCO2
                "Seoul Solar Farm"
            );
            
            expect(await energyNFT.ownerOf(1)).to.equal(recipient.address);
        });
    });

    describe("민팅", function () {
        const tokenURI = "ipfs://QmTest123";
        const energyAmount = 1500; // 1.5 MWh (kWh 단위)
        const carbonOffset = 699; // 0.699 tCO2 (1000배)
        const energyType = "solar";
        const location = "경기도 화성시 태양광발전소";

        it("소유자가 NFT를 민팅할 수 있어야 함", async function () {
            await expect(energyNFT.mintEnergyNFT(
                recipient.address,
                tokenURI,
                energyAmount,
                supplier.address,
                buyer.address,
                energyType,
                carbonOffset,
                location
            )).to.emit(energyNFT, "EnergyNFTMinted");

            expect(await energyNFT.ownerOf(1)).to.equal(recipient.address);
            expect(await energyNFT.tokenURI(1)).to.equal(tokenURI);
        });

        it("소유자가 아닌 사용자는 민팅할 수 없어야 함", async function () {
            await expect(energyNFT.connect(buyer).mintEnergyNFT(
                recipient.address,
                tokenURI,
                energyAmount,
                supplier.address,
                buyer.address,
                energyType,
                carbonOffset,
                location
            )).to.be.revertedWith("Ownable: caller is not the owner");
        });

        it("에너지 데이터가 올바르게 저장되어야 함", async function () {
            await energyNFT.mintEnergyNFT(
                recipient.address,
                tokenURI,
                energyAmount,
                supplier.address,
                buyer.address,
                energyType,
                carbonOffset,
                location
            );

            const energyData = await energyNFT.getEnergyData(1);
            expect(energyData.energyAmount).to.equal(energyAmount);
            expect(energyData.supplier).to.equal(supplier.address);
            expect(energyData.buyer).to.equal(buyer.address);
            expect(energyData.energyType).to.equal(energyType);
            expect(energyData.carbonOffset).to.equal(carbonOffset);
            expect(energyData.location).to.equal(location);
            expect(energyData.isRetired).to.equal(false);
        });

        it("민팅 시 이벤트가 발생해야 함", async function () {
            await expect(energyNFT.mintEnergyNFT(
                recipient.address,
                tokenURI,
                energyAmount,
                supplier.address,
                buyer.address,
                energyType,
                carbonOffset,
                location
            )).to.emit(energyNFT, "EnergyNFTMinted")
              .withArgs(1, supplier.address, buyer.address, energyAmount, energyType);
        });
    });

    describe("NFT 은퇴", function () {
        beforeEach(async function () {
            // 테스트용 NFT 민팅
            await energyNFT.mintEnergyNFT(
                recipient.address,
                "ipfs://QmTest123",
                1000,
                supplier.address,
                buyer.address,
                "solar",
                466,
                "Test Location"
            );
        });

        it("NFT 소유자가 은퇴할 수 있어야 함", async function () {
            await expect(energyNFT.connect(recipient).retireNFT(1))
                .to.emit(energyNFT, "EnergyNFTRetired")
                .withArgs(1, recipient.address);

            const energyData = await energyNFT.getEnergyData(1);
            expect(energyData.isRetired).to.equal(true);
        });

        it("NFT 소유자가 아닌 사용자는 은퇴할 수 없어야 함", async function () {
            await expect(energyNFT.connect(buyer).retireNFT(1))
                .to.be.revertedWith("Only owner can retire NFT");
        });

        it("이미 은퇴한 NFT는 다시 은퇴할 수 없어야 함", async function () {
            await energyNFT.connect(recipient).retireNFT(1);
            
            await expect(energyNFT.connect(recipient).retireNFT(1))
                .to.be.revertedWith("NFT already retired");
        });
    });

    describe("탄소 회피량 계산", function () {
        beforeEach(async function () {
            // 여러 NFT 민팅
            await energyNFT.mintEnergyNFT(
                recipient.address,
                "ipfs://QmTest1",
                1000, // 1 MWh
                supplier.address,
                buyer.address,
                "solar",
                466, // 0.466 tCO2
                "Location 1"
            );

            await energyNFT.mintEnergyNFT(
                recipient.address,
                "ipfs://QmTest2",
                2000, // 2 MWh
                supplier.address,
                buyer.address,
                "wind",
                22, // 0.022 tCO2
                "Location 2"
            );
        });

        it("총 탄소 회피량을 올바르게 계산해야 함", async function () {
            const totalOffset = await energyNFT.getTotalCarbonOffset(recipient.address);
            expect(totalOffset).to.equal(488); // 466 + 22
        });

        it("은퇴한 NFT는 탄소 회피량에서 제외되어야 함", async function () {
            await energyNFT.connect(recipient).retireNFT(1);
            
            const totalOffset = await energyNFT.getTotalCarbonOffset(recipient.address);
            expect(totalOffset).to.equal(22); // 22만 남음
        });

        it("NFT가 없는 주소의 탄소 회피량은 0이어야 함", async function () {
            const totalOffset = await energyNFT.getTotalCarbonOffset(buyer.address);
            expect(totalOffset).to.equal(0);
        });
    });

    describe("일시정지 기능", function () {
        it("소유자가 컨트랙트를 일시정지할 수 있어야 함", async function () {
            await energyNFT.pause();
            expect(await energyNFT.paused()).to.equal(true);
        });

        it("일시정지 상태에서는 민팅할 수 없어야 함", async function () {
            await energyNFT.pause();
            
            await expect(energyNFT.mintEnergyNFT(
                recipient.address,
                "ipfs://QmTest",
                1000,
                supplier.address,
                buyer.address,
                "solar",
                466,
                "Test Location"
            )).to.be.revertedWith("Pausable: paused");
        });

        it("일시정지 상태에서는 전송할 수 없어야 함", async function () {
            // 먼저 NFT 민팅
            await energyNFT.mintEnergyNFT(
                recipient.address,
                "ipfs://QmTest",
                1000,
                supplier.address,
                buyer.address,
                "solar",
                466,
                "Test Location"
            );

            // 컨트랙트 일시정지
            await energyNFT.pause();

            // 전송 시도
            await expect(energyNFT.connect(recipient).transferFrom(
                recipient.address,
                buyer.address,
                1
            )).to.be.revertedWith("Pausable: paused");
        });

        it("소유자가 일시정지를 해제할 수 있어야 함", async function () {
            await energyNFT.pause();
            await energyNFT.unpause();
            expect(await energyNFT.paused()).to.equal(false);
        });
    });

    describe("접근 제어", function () {
        it("소유자가 아닌 사용자는 일시정지할 수 없어야 함", async function () {
            await expect(energyNFT.connect(buyer).pause())
                .to.be.revertedWith("Ownable: caller is not the owner");
        });

        it("소유자가 아닌 사용자는 일시정지를 해제할 수 없어야 함", async function () {
            await energyNFT.pause();
            await expect(energyNFT.connect(buyer).unpause())
                .to.be.revertedWith("Ownable: caller is not the owner");
        });
    });

    describe("토큰 조회", function () {
        it("존재하지 않는 토큰 조회 시 에러가 발생해야 함", async function () {
            await expect(energyNFT.getEnergyData(999))
                .to.be.revertedWith("Token does not exist");
        });

        it("토큰 URI를 올바르게 반환해야 함", async function () {
            const tokenURI = "ipfs://QmTest123";
            await energyNFT.mintEnergyNFT(
                recipient.address,
                tokenURI,
                1000,
                supplier.address,
                buyer.address,
                "solar",
                466,
                "Test Location"
            );

            expect(await energyNFT.tokenURI(1)).to.equal(tokenURI);
        });
    });

    describe("ERC721 기능", function () {
        beforeEach(async function () {
            await energyNFT.mintEnergyNFT(
                recipient.address,
                "ipfs://QmTest123",
                1000,
                supplier.address,
                buyer.address,
                "solar",
                466,
                "Test Location"
            );
        });

        it("NFT를 전송할 수 있어야 함", async function () {
            await energyNFT.connect(recipient).transferFrom(
                recipient.address,
                buyer.address,
                1
            );

            expect(await energyNFT.ownerOf(1)).to.equal(buyer.address);
        });

        it("승인 후 제3자가 전송할 수 있어야 함", async function () {
            await energyNFT.connect(recipient).approve(buyer.address, 1);
            await energyNFT.connect(buyer).transferFrom(
                recipient.address,
                supplier.address,
                1
            );

            expect(await energyNFT.ownerOf(1)).to.equal(supplier.address);
        });

        it("잔액을 올바르게 반환해야 함", async function () {
            expect(await energyNFT.balanceOf(recipient.address)).to.equal(1);
            expect(await energyNFT.balanceOf(buyer.address)).to.equal(0);
        });
    });
});