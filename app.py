from google.cloud import firestore
import streamlit as st
import pandas as pd

chapters = [f'ch0{i}' for i in range(2, 4)]
chapters.extend(['ch04-1', 'ch04-2'])
chapters.extend([f'ch0{i}' for i in range(5, 8)])
names = []
a = {}
b = {}

DB = firestore.Client.from_service_account_json("key.json")

#학회원 name 가져오기
collection = DB.collection('ch02')
for i in collection.stream():
    names.append(i.id)

#한 챕터 과제체크 df
def one_chapter(chapter:str, dict:dict) -> dict:
    collection = DB.collection(chapter)
    dict[chapter] = []


    for name in names:
        doc_ref = collection.document(name)
        doc_field = doc_ref.get().to_dict()

        if "FINAL_SUBMIT" in doc_field:
            dict[chapter].append('O')
        else:
            dict[chapter].append('')
    return dict


#챕터별 학회원 답변 보여주는 함수
def answer_check(chapter:str):
    collection = DB.collection(chapter)
    a = [f'Q{i}' for i in range(1, 9)]
    qs = ['FINAL SUBMIT'] + a
    ans = {}

    for name in names:
        doc_ref = collection.document(name)
        doc_field = doc_ref.get().to_dict()
        ans[name] = {}

        for q in qs:
            a = doc_field.get(q)
            if a:
                ans[name][q] = a
            else:
                ans[name][q] = ''

    for name in names:
        st.subheader(name)
        st.write(ans[name], unsafe_allow_html=True)


if __name__ == "__main__":

    #챕터 선택하는 사이드바
    with st.sidebar:
        selected = st.selectbox("챕터 선택",
                                chapters)
        
    #챕터별 과제 제출 여부를 담은 데이터프레임 반환
    for chapter in chapters:
        x = one_chapter(chapter, a)  #x = {'ch02': ['O','','O','' ,,,]}

    #모든 챕터 제출여부를 담은 데이터프레임 그리기
    df = pd.DataFrame(x, index = names)
    st.dataframe(df, height = 600)

    #사이드바에서 선택한 한 챕터 과제제출 여부를 담은 데이터프레임
    y = one_chapter(selected, b)

    df = pd.DataFrame(y, index = names)
    st.dataframe(df, height = 600)
    
    #selected된 챕터의 학회원 정답 보여주기
    answer_check(selected)





        

