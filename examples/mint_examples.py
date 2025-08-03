#!/usr/bin/env python3
"""
에너지 인증서 NFT 민팅 예시 스크립트
다양한 실제 사용 사례를 보여주는 예제들
"""

import sys
import os
import time
from datetime import datetime, timedelta

# 상위 디렉토리의 python 모듈 import를 위한 경로 추가
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'python'))

from energy_nft_minter import EnergyNFTMinter

def example_1_basic_solar_trade():
    """
    예시 1: 기본 태양광 전력 거래
    중소기업이 태양광 발전소에서 전력을 구매하는 경우
    """
    print("🌞 예시 1: 기본 태양광 전력 거래")
    print("=" * 50)
    
    minter = EnergyNFTMinter("python/config.json")
    
    energy_data = {
        "energy_amount": 1.5,  # 1.5 MWh
        "energy_type": "solar",
        "supplier": "0x742d35Cc6634C0532925a3b8D7e99B8fF4b4c4C7",  # 태양광 발전소
        "buyer": "0x8ba1f109551bD432803012645Hac136c903C2B3F",      # 중소기업
        "location": "경기도 화성시 태양광발전소",
        "timestamp": datetime.now().isoformat(),
        "country": "South Korea",
        "year": 2024
    }
    
    try:
        tx_hash = minter.mint_nft(energy_data)
        print(f"✅ 태양광 NFT 민팅 성공!")
        print(f"📄 거래량: {energy_data['energy_amount']} MWh")
        print(f"🌱 예상 탄소 회피량: {energy_data['energy_amount'] * 0.466:.3f} tCO₂")
        print(f"🔗 트랜잭션: {tx_hash}")
        print()
    except Exception as e:
        print(f"❌ 민팅 실패: {e}")

def example_2_re100_corporate_purchase():
    """
    예시 2: RE100 기업의 대규모 재생에너지 구매
    글로벌 기업이 연간 전력 수요의 일부를 재생에너지로 충당
    """
    print("🏢 예시 2: RE100 기업의 대규모 재생에너지 구매")
    print("=" * 50)
    
    minter = EnergyNFTMinter("python/config.json")
    
    # 삼성전자가 다양한 재생에너지를 구매하는 시나리오
    purchases = [
        {
            "energy_amount": 50.0,  # 50 MWh
            "energy_type": "solar",
            "supplier": "0x123SolarFarm456",
            "buyer": "0xSamsungElectronics",
            "location": "전남 신안군 해상태양광단지",
            "description": "삼성전자 천안캠퍼스 전력공급"
        },
        {
            "energy_amount": 75.0,  # 75 MWh
            "energy_type": "wind",
            "supplier": "0x789WindFarmABC",
            "buyer": "0xSamsungElectronics",
            "location": "제주도 해상풍력단지",
            "description": "삼성전자 기흥캠퍼스 전력공급"
        },
        {
            "energy_amount": 30.0,  # 30 MWh
            "energy_type": "hydro",
            "supplier": "0xDEFHydroPowerGHI",
            "buyer": "0xSamsungElectronics",
            "location": "강원도 춘천 수력발전소",
            "description": "삼성전자 화성캠퍼스 전력공급"
        }
    ]
    
    total_energy = 0
    total_carbon_offset = 0
    
    for i, purchase in enumerate(purchases, 1):
        energy_data = {
            **purchase,
            "timestamp": (datetime.now() + timedelta(hours=i)).isoformat(),
            "country": "South Korea",
            "year": 2024
        }
        
        # 탄소 회피량 계산
        carbon_factors = {"solar": 0.466, "wind": 0.011, "hydro": 0.024}
        carbon_offset = energy_data["energy_amount"] * carbon_factors[energy_data["energy_type"]]
        
        try:
            tx_hash = minter.mint_nft(energy_data)
            print(f"✅ {energy_data['energy_type'].upper()} NFT #{i} 민팅 성공!")
            print(f"📄 거래량: {energy_data['energy_amount']} MWh")
            print(f"🌱 탄소 회피량: {carbon_offset:.3f} tCO₂")
            print(f"📍 위치: {energy_data['location']}")
            print(f"🔗 트랜잭션: {tx_hash}")
            print(f"💼 용도: {energy_data['description']}")
            
            total_energy += energy_data["energy_amount"]
            total_carbon_offset += carbon_offset
            
            # API 레이트 제한 방지
            time.sleep(3)
            
        except Exception as e:
            print(f"❌ {energy_data['energy_type']} NFT 민팅 실패: {e}")
        
        print("-" * 30)
    
    print(f"📊 RE100 구매 요약:")
    print(f"   총 재생에너지: {total_energy} MWh")
    print(f"   총 탄소 회피량: {total_carbon_offset:.3f} tCO₂")
    print(f"   구매 건수: {len(purchases)}건")
    print()

def example_3_cbam_export_compliance():
    """
    예시 3: CBAM 대응을 위한 수출기업 사례
    철강회사가 EU 수출을 위해 생산과정 재생에너지 사용량 추적
    """
    print("🏭 예시 3: CBAM 대응을 위한 수출기업 사례")
    print("=" * 50)
    
    minter = EnergyNFTMinter("python/config.json")
    
    # 포스코가 철강 생산 과정에서 사용한 재생에너지
    production_processes = [
        {
            "process": "철광석 소결",
            "energy_amount": 25.0,  # 25 MWh
            "energy_type": "hydro",
            "location": "포항제철소"
        },
        {
            "process": "고로 용해",
            "energy_amount": 40.0,  # 40 MWh
            "energy_type": "solar",
            "location": "포항제철소"
        },
        {
            "process": "압연 공정",
            "energy_amount": 15.0,  # 15 MWh
            "energy_type": "wind",
            "location": "포항제철소"
        },
        {
            "process": "품질 검사",
            "energy_amount": 5.0,   # 5 MWh
            "energy_type": "biomass",
            "location": "포항제철소"
        }
    ]
    
    print(f"🎯 목적: EU 수출 철강재 CBAM 신고용 재생에너지 사용량 증명")
    print(f"🏢 회사: 포스코 (POSCO)")
    print(f"📦 제품: 자동차용 냉연강판 1,000톤")
    print()
    
    total_production_energy = 0
    total_production_carbon = 0
    
    for i, process in enumerate(production_processes, 1):
        energy_data = {
            "energy_amount": process["energy_amount"],
            "energy_type": process["energy_type"],
            "supplier": "0xRenewableEnergyProvider",
            "buyer": "0xPOSCO",
            "location": f"{process['location']} - {process['process']}",
            "timestamp": (datetime.now() + timedelta(minutes=i*30)).isoformat(),
            "country": "South Korea",
            "year": 2024,
            "production_process": process["process"]
        }
        
        # 탄소 회피량 계산
        carbon_factors = {"solar": 0.466, "wind": 0.011, "hydro": 0.024, "biomass": 0.18}
        carbon_offset = energy_data["energy_amount"] * carbon_factors[energy_data["energy_type"]]
        
        try:
            tx_hash = minter.mint_nft(energy_data)
            print(f"✅ 공정 #{i}: {process['process']} NFT 민팅 성공!")
            print(f"⚡ {energy_data['energy_type'].upper()}: {energy_data['energy_amount']} MWh")
            print(f"🌱 탄소 회피: {carbon_offset:.3f} tCO₂")
            print(f"🔗 TX: {tx_hash}")
            
            total_production_energy += energy_data["energy_amount"]
            total_production_carbon += carbon_offset
            
            time.sleep(2)
            
        except Exception as e:
            print(f"❌ {process['process']} NFT 민팅 실패: {e}")
        
        print("-" * 25)
    
    # CBAM 신고서 요약
    steel_production_tons = 1000  # 1,000톤
    energy_intensity = total_production_energy / steel_production_tons  # MWh/ton
    carbon_intensity = total_production_carbon / steel_production_tons   # tCO2/ton
    
    print(f"📋 CBAM 신고서 요약:")
    print(f"   제품: 냉연강판 {steel_production_tons}톤")
    print(f"   총 재생에너지 사용량: {total_production_energy} MWh")
    print(f"   총 탄소 회피량: {total_production_carbon:.3f} tCO₂")
    print(f"   에너지 집약도: {energy_intensity:.3f} MWh/톤")
    print(f"   탄소 집약도: {carbon_intensity:.6f} tCO₂/톤")
    print(f"   🇪🇺 EU 탄소국경세 절약 예상액: ${total_production_carbon * 85:.2f} USD")
    print()

def example_4_monthly_esg_reporting():
    """
    예시 4: 월간 ESG 보고를 위한 재생에너지 구매
    상장기업이 매월 ESG 보고서 작성을 위해 재생에너지 구매량 추적
    """
    print("📊 예시 4: 월간 ESG 보고를 위한 재생에너지 구매")
    print("=" * 50)
    
    minter = EnergyNFTMinter("python/config.json")
    
    # LG전자의 월간 재생에너지 구매 데이터 (3개월)
    monthly_purchases = [
        {
            "month": "2024-01",
            "energy_amount": 120.0,  # 120 MWh
            "energy_type": "solar",
            "description": "LG전자 평택캠퍼스 1월 전력공급"
        },
        {
            "month": "2024-02", 
            "energy_amount": 110.0,  # 110 MWh
            "energy_type": "wind",
            "description": "LG전자 창원캠퍼스 2월 전력공급"
        },
        {
            "month": "2024-03",
            "energy_amount": 135.0,  # 135 MWh
            "energy_type": "hydro",
            "description": "LG전자 구미캠퍼스 3월 전력공급"
        }
    ]
    
    print(f"🎯 목적: 분기별 ESG 보고서 작성용 재생에너지 사용량 입증")
    print(f"🏢 회사: LG전자")
    print(f"📅 기간: 2024년 1분기 (1-3월)")
    print()
    
    quarterly_total_energy = 0
    quarterly_total_carbon = 0
    
    for i, purchase in enumerate(monthly_purchases, 1):
        # 월별 첫째 날 오전 9시로 설정
        month_start = datetime(2024, i, 1, 9, 0, 0)
        
        energy_data = {
            "energy_amount": purchase["energy_amount"],
            "energy_type": purchase["energy_type"],
            "supplier": f"0xRenewableProvider{i:03d}",
            "buyer": "0xLGElectronics",
            "location": f"전국 {purchase['energy_type']} 발전단지",
            "timestamp": month_start.isoformat(),
            "country": "South Korea",
            "year": 2024,
            "reporting_period": purchase["month"],
            "purpose": "ESG_REPORTING"
        }
        
        # 탄소 회피량 계산
        carbon_factors = {"solar": 0.466, "wind": 0.011, "hydro": 0.024}
        carbon_offset = energy_data["energy_amount"] * carbon_factors[energy_data["energy_type"]]
        
        try:
            tx_hash = minter.mint_nft(energy_data)
            print(f"✅ {purchase['month']} {energy_data['energy_type'].upper()} NFT 민팅 성공!")
            print(f"📄 월간 구매량: {energy_data['energy_amount']} MWh")
            print(f"🌱 월간 탄소 회피: {carbon_offset:.3f} tCO₂")
            print(f"💼 {purchase['description']}")
            print(f"🔗 TX: {tx_hash}")
            
            quarterly_total_energy += energy_data["energy_amount"]
            quarterly_total_carbon += carbon_offset
            
            time.sleep(2)
            
        except Exception as e:
            print(f"❌ {purchase['month']} NFT 민팅 실패: {e}")
        
        print("-" * 30)
    
    # ESG KPI 계산
    employee_count = 75000  # LG전자 임직원 수
    revenue_billion = 63    # 연매출 (조원)
    energy_per_employee = quarterly_total_energy / employee_count * 1000  # kWh/임직원
    carbon_per_revenue = quarterly_total_carbon / revenue_billion  # tCO2/조원
    
    print(f"📋 1분기 ESG 보고서 KPI:")
    print(f"   분기 재생에너지 총 사용량: {quarterly_total_energy} MWh")
    print(f"   분기 탄소 회피량: {quarterly_total_carbon:.3f} tCO₂")
    print(f"   임직원당 재생에너지 사용량: {energy_per_employee:.3f} kWh/명")
    print(f"   매출 조원당 탄소 회피량: {carbon_per_revenue:.6f} tCO₂/조원")
    print(f"   🌟 재생에너지 비율: 15.2% (목표: 20%)")
    print()

def example_5_carbon_credit_trading():
    """
    예시 5: 탄소 크레딧 거래소 활용
    기업이 보유한 재생에너지 NFT를 은퇴시켜 탄소 크레딧으로 활용
    """
    print("💱 예시 5: 탄소 크레딧 거래소 활용")
    print("=" * 50)
    
    print("🎯 시나리오: 현대자동차가 보유한 재생에너지 NFT를 탄소 크레딧으로 전환")
    print("📦 목적: 차량 생산 과정의 탄소 중립 달성")
    print()
    
    # 주의: 실제 은퇴 기능 구현을 위해서는 스마트컨트랙트의 retireNFT 함수 호출 필요
    # 여기서는 시나리오만 설명
    
    retirement_scenarios = [
        {
            "token_id": 1,
            "energy_amount": 50.0,
            "energy_type": "solar",
            "carbon_offset": 23.3,  # 50 * 0.466
            "retirement_purpose": "소나타 하이브리드 1,000대 생산 탄소상쇄"
        },
        {
            "token_id": 2,
            "energy_amount": 100.0,
            "energy_type": "wind",
            "carbon_offset": 1.1,   # 100 * 0.011
            "retirement_purpose": "아이오닉5 500대 생산 탄소상쇄"
        },
        {
            "token_id": 3,
            "energy_amount": 75.0,
            "energy_type": "hydro",
            "carbon_offset": 1.8,   # 75 * 0.024
            "retirement_purpose": "제네시스 G90 200대 생산 탄소상쇄"
        }
    ]
    
    total_retired_energy = 0
    total_carbon_credits = 0
    
    for scenario in retirement_scenarios:
        print(f"🔥 NFT #{scenario['token_id']} 은퇴 처리")
        print(f"   에너지원: {scenario['energy_type'].upper()}")
        print(f"   전력량: {scenario['energy_amount']} MWh")
        print(f"   탄소 크레딧: {scenario['carbon_offset']} tCO₂")
        print(f"   사용 목적: {scenario['retirement_purpose']}")
        print(f"   💰 크레딧 가치: ${scenario['carbon_offset'] * 85:.2f} USD")
        
        total_retired_energy += scenario['energy_amount']
        total_carbon_credits += scenario['carbon_offset']
        
        print("-" * 30)
    
    print(f"📊 탄소 크레딧 거래 요약:")
    print(f"   은퇴된 재생에너지 NFT: 3개")
    print(f"   총 재생에너지량: {total_retired_energy} MWh")
    print(f"   생성된 탄소 크레딧: {total_carbon_credits:.1f} tCO₂")
    print(f"   💰 총 크레딧 가치: ${total_carbon_credits * 85:.2f} USD")
    print(f"   🚗 탄소중립 차량 생산: 1,700대")
    print()

def main():
    """메인 실행 함수"""
    print("🌱 Energy Certificate NFT 민팅 예시 모음")
    print("=" * 60)
    print("다양한 실제 사용 사례를 통한 NFT 민팅 데모")
    print()
    
    examples = [
        ("기본 태양광 전력 거래", example_1_basic_solar_trade),
        ("RE100 기업의 대규모 구매", example_2_re100_corporate_purchase),
        ("CBAM 대응 수출기업", example_3_cbam_export_compliance),
        ("월간 ESG 보고", example_4_monthly_esg_reporting),
        ("탄소 크레딧 거래", example_5_carbon_credit_trading)
    ]
    
    print("📋 실행할 예시를 선택하세요:")
    for i, (title, _) in enumerate(examples, 1):
        print(f"   {i}. {title}")
    print("   0. 모든 예시 실행")
    print()
    
    try:
        choice = input("선택 (0-5): ").strip()
        
        if choice == "0":
            print("🚀 모든 예시를 순차적으로 실행합니다...\n")
            for title, func in examples:
                print(f"▶️ {title} 시작")
                func()
                print("⏸️ 다음 예시를 위해 5초 대기...\n")
                time.sleep(5)
        elif choice in ["1", "2", "3", "4", "5"]:
            idx = int(choice) - 1
            title, func = examples[idx]
            print(f"🚀 {title} 예시를 실행합니다...\n")
            func()
        else:
            print("❌ 잘못된 선택입니다.")
            
    except KeyboardInterrupt:
        print("\n👋 사용자에 의해 중단되었습니다.")
    except Exception as e:
        print(f"\n❌ 실행 중 오류 발생: {e}")
    
    print("✅ 예시 실행 완료!")
    print("📚 더 많은 정보는 README.md를 참조하세요.")

if __name__ == "__main__":
    main()