// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/Pausable.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

contract EnergyCertificateNFT is ERC721URIStorage, ERC721Enumerable, Ownable, Pausable, ReentrancyGuard {
    uint256 private _tokenIdCounter;
    
    // 에너지 거래 정보 구조체
    struct EnergyData {
        uint256 energyAmount;      // MWh 단위
        uint256 timestamp;         // 거래 시간
        address supplier;          // 공급자 주소
        address buyer;            // 구매자 주소
        string energyType;        // 에너지 타입 (solar, wind, hydro 등)
        uint256 carbonOffset;     // 탄소 회피량 (tCO2)
        string location;          // 발전소 위치
        bool isRetired;          // 은퇴 여부 (중복 사용 방지)
    }
    
    // 토큰별 에너지 데이터 매핑
    mapping(uint256 => EnergyData) public energyData;
    
    // 이벤트 정의
    event EnergyNFTMinted(
        uint256 indexed tokenId,
        address indexed supplier,
        address indexed buyer,
        uint256 energyAmount,
        string energyType
    );
    
    event EnergyNFTRetired(
        uint256 indexed tokenId,
        address indexed owner
    );
    
    constructor() ERC721("EnergyCertificateNFT", "ECN") {
        _tokenIdCounter = 1; // 1부터 시작
    }
    
    /**
     * @dev 에너지 NFT 민팅
     * @param recipient NFT를 받을 주소
     * @param tokenURI 메타데이터 URI (IPFS)
     * @param _energyAmount 에너지량 (MWh)
     * @param _supplier 공급자 주소
     * @param _buyer 구매자 주소
     * @param _energyType 에너지 타입
     * @param _carbonOffset 탄소 회피량
     * @param _location 발전소 위치
     */
    function mintEnergyNFT(
        address recipient,
        string memory tokenURI,
        uint256 _energyAmount,
        address _supplier,
        address _buyer,
        string memory _energyType,
        uint256 _carbonOffset,
        string memory _location
    ) public onlyOwner whenNotPaused returns (uint256) {
        uint256 tokenId = _tokenIdCounter;
        
        _safeMint(recipient, tokenId);
        _setTokenURI(tokenId, tokenURI);
        
        // 에너지 데이터 저장
        energyData[tokenId] = EnergyData({
            energyAmount: _energyAmount,
            timestamp: block.timestamp,
            supplier: _supplier,
            buyer: _buyer,
            energyType: _energyType,
            carbonOffset: _carbonOffset,
            location: _location,
            isRetired: false
        });
        
        _tokenIdCounter++;
        
        emit EnergyNFTMinted(tokenId, _supplier, _buyer, _energyAmount, _energyType);
        
        return tokenId;
    }
    
    /**
     * @dev NFT 은퇴 (중복 사용 방지를 위한 소각)
     * @param tokenId 은퇴할 NFT ID
     */
    function retireNFT(uint256 tokenId) public {
        require(ownerOf(tokenId) == msg.sender, "Only owner can retire NFT");
        require(!energyData[tokenId].isRetired, "NFT already retired");
        
        energyData[tokenId].isRetired = true;
        
        emit EnergyNFTRetired(tokenId, msg.sender);
    }
    
    /**
     * @dev 에너지 데이터 조회
     */
    function getEnergyData(uint256 tokenId) public view returns (EnergyData memory) {
        require(_exists(tokenId), "Token does not exist");
        return energyData[tokenId];
    }
    
    /**
     * @dev 총 탄소 회피량 계산 (특정 주소가 보유한 NFT들의 합계)
     */
    function getTotalCarbonOffset(address owner) public view returns (uint256) {
        uint256 balance = balanceOf(owner);
        uint256 totalOffset = 0;
        
        for (uint256 i = 0; i < balance; i++) {
            uint256 tokenId = tokenOfOwnerByIndex(owner, i);
            if (!energyData[tokenId].isRetired) {
                totalOffset += energyData[tokenId].carbonOffset;
            }
        }
        
        return totalOffset;
    }
    
    /**
     * @dev 관리자 기능: 일시정지
     */
    function pause() public onlyOwner {
        _pause();
    }
    
    function unpause() public onlyOwner {
        _unpause();
    }
    
    // OpenZeppelin 오버라이드 함수들
    function _beforeTokenTransfer(
        address from,
        address to,
        uint256 tokenId,
        uint256 batchSize
    ) internal override(ERC721, ERC721Enumerable) whenNotPaused {
        super._beforeTokenTransfer(from, to, tokenId, batchSize);
    }
    
    function _burn(uint256 tokenId) internal override(ERC721, ERC721URIStorage) {
        super._burn(tokenId);
    }
    
    function tokenURI(uint256 tokenId)
        public
        view
        override(ERC721, ERC721URIStorage)
        returns (string memory)
    {
        return super.tokenURI(tokenId);
    }
    
    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(ERC721, ERC721Enumerable, ERC721URIStorage)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }
}