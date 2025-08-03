const hre = require("hardhat");

async function main() {
  console.log("🚀 에너지 인증서 NFT 배포 시작...");
  
  // 컨트랙트 팩토리 가져오기
  const EnergyCertificateNFT = await hre.ethers.getContractFactory("EnergyCertificateNFT");
  
  // 배포
  console.log("📦 컨트랙트 배포 중...");
  const energyNFT = await EnergyCertificateNFT.deploy();
  
  // 배포 완료 대기
  await energyNFT.waitForDeployment();
  
  const contractAddress = await energyNFT.getAddress();
  console.log("✅ EnergyCertificateNFT 배포 완료!");
  console.log("📍 컨트랙트 주소:", contractAddress);
  
  // 네트워크 정보 출력
  const network = await hre.ethers.provider.getNetwork();
  console.log("🌐 네트워크:", network.name);
  console.log("🆔 체인 ID:", network.chainId);
  
  // 배포자 정보
  const [deployer] = await hre.ethers.getSigners();
  console.log("👤 배포자 주소:", deployer.address);
  
  // 컨트랙트 초기 정보 확인
  const name = await energyNFT.name();
  const symbol = await energyNFT.symbol();
  console.log("🏷️ NFT 이름:", name);
  console.log("🔖 NFT 심볼:", symbol);
  
  // 검증을 위한 정보 저장
  const deploymentInfo = {
    contractAddress: contractAddress,
    network: network.name,
    chainId: network.chainId.toString(),
    deployer: deployer.address,
    blockNumber: await hre.ethers.provider.getBlockNumber(),
    timestamp: new Date().toISOString(),
    constructorArgs: [] // 생성자 인수가 없음
  };
  
  console.log("\n📋 배포 정보:");
  console.log(JSON.stringify(deploymentInfo, null, 2));
  
  // 환경별 추가 안내
  if (network.name === "sepolia" || network.name === "polygon" || network.name === "mumbai") {
    console.log("\n🔍 Etherscan/Polygonscan 검증 명령어:");
    console.log(`npx hardhat verify --network ${network.name} ${contractAddress}`);
  }
  
  console.log("\n🎉 배포가 성공적으로 완료되었습니다!");
}

// 에러 처리
main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error("❌ 배포 실패:", error);
    process.exit(1);
  });