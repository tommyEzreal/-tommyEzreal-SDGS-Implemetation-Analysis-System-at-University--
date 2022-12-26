# NLP를 활용한 대학의 SDGs 이행 분석 시스템

## Description

딥러닝 기술을 활용하여 대학의 SDGs 이행 분석 시스템을 개발하였습니다.
BERT를 이용하여 개별 목표에 해당하는 사례에 대한 분류를 진행하였으며, 해외 대학과 국내 대학의 이행 사례에 대한 키워드 추출에는 TextRank를 사용하였습니다. 
마지막으로 TF-IDF와 코사인 유사도를 활용하여 국내 대학이 참고할 수 있는 해외 대학 사례 제시해주고자 하였습니다. 
결과적으로 각 대학의 SDGs 이행 현황을 분석하고, 나아가 참고할 수 있는 해외 사례들을 제시해주어 국내 대학의 SDGs 이행에 참고가 될 수 있는 웹사이트를 구현하였습니다. 

### About SDGs
 - SDGs(Sustainable Development Goals)는 UN에서 전 세계가 지속가능한 발전을 위해 2030년까지 달성하기로 합의한 목표입니다.
 - 17 Goals<br>
 1)빈곤종식 2)기아종식 3)건강과 웰빙 4)양질의 교육 5)성평등 6)깨끗한 물과 위생 7)모두를 위한 깨끗한 에너지 8)양질의 일자리와 경제성장
 9)산업, 혁신 사회기반 시설 10)불평등 감소 11)지속가능한 도시와 공동체 12)지속가능한 생산과 소비 13)기후변하 대응 14)해양 생태계 보존
 15)육상 생태계 보호 16)정의, 평화, 효과적인 제도 17)글로벌 파트너십
 - 5P<br>
 사람(People) | 1, 2, 3, 4, 5<br>
 지구(Planet) | 6, 12, 13, 14, 15<br>
 번영(Prosperity) | 7, 8, 9, 10, 11<br>
 평화(Peace) |16<br>
 협력(Partnership) | 17<br>



## Data

- 해외 73개 대학 SDGs 보고서 92편
- 국내 15개 대학 홈페이지 뉴스기사 15000편

## Prerequisites

- python 3.8
- 설치 모듈 상세정보는 requirements.txt 파일 참고
- 한국어 띄어쓰기 패키지 PyKoSpacing 추가 설치 필요

```
pip install -r requirements.txt
pip install git+https://github.com/haven-jeon/PyKoSpacing.git
```

## Methodology
<img width="700" alt="스크린샷 2022-11-06 오후 9 47 32" src="https://user-images.githubusercontent.com/91872769/200171603-6a40263c-2939-40d5-9110-9fd28b8d71e2.png">

## Classification Model Accuracy

|증강기법|증강미적용|RI|RD|RI+BT|BT|
|-|-|-|-|-|-|
|Accuracy|0.68|0.64|0.71|0.72|0.79|

## Website

### URL
https://hajin0324.github.io/SustainED/

### Dashboard Description
- 영국 글로벌 대학 평가기관인 THE(Times Higher Education)가 발표한 2022년도 세계 대학 영향력 평가점수 및 3개년 점수 추이 그래프
- 자동분류모델을 통해 도출한 5P 항목별 뉴스 기사의 비율을 나타내는 파이 그래프
- 5P 부문별 대학의 Impact Rankings 2022 점수와 국내 전체 대학 및 해외 전체 대학의 평균 점수
- 5P 항목별 TextRank와 KeyBERT 기반의 키워드 분포
- 해당 대학에는 존재하지 않는 타 대학들의 키워드를 유사도 기반 벤치마크 알고리즘을 이용해 대학별로 참고할 수 있는 사례 제시



 

## Reference

-  Lee, H.: Necessity and Challenges of Sustainable Development Education(ESD) and SDGs Education in Universities. The Journal of Liberal Arts, 12, 257-284 (2020).
- Kim, A., Jung, Y.: Classification of themes of domestic music using KoBERT. Proceedings of the Korean Information Science Society Conference, pp. 1738-1740 (2021).
- Devlin, J., Chang, M., Lee, K., Toutanova, K.: BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding. Google AI Language, 1-16 (2019).
- Wei, J., Zou, K.: EDA: Easy Data Augmentation Techniques for Boosting Performance on Text Classification Tasks. Protago Labs Research, Tysons Corner, Virginia, USA, Department of Computer Science, Dartmouth College, Department of Mathematics and Statistics, Georgetown University, 1-9 (2019).
- Edunov, S., Ott, M., Auli, M., Grangier, D.: Understanding Back-Translation at Scale. Facebook AI Research, Menlo Park, CA & New York, NY, Google Brain, Mountain View, CA, 1-12 (2018).
- Mihalcea, R., Tarau, P.: TextRank: Bringing Order into Texts. Department of Computer Science University of North Texas, 1-8 (2004).
- Zhang, J., Zhao, Y., Saleh, M., Liu, P. J.: PEGASUS: Pre-training with Extracted Gap-sentences for Abstractive Summarization. Data Science Institute, Imperial College London, London, UK, Brain Team, Google Research, Mountain View, 1-55 (2020).
- 'TextRank 를 이용한 키워드 추출과 핵심 문장 추출 (구현과 실험).' LOVIT x DATA SCIENCE. last modified Apr 30, 2019, accessed Aug 20, 2022, https://lovit.github.io/nlp/2019/04/30/textrank/
