import mysql.connector

def search_player_info(player_name, year, position):
    try:
        # MySQL 연결 설정
        db_config = {
            'host': 'localhost',
            'user': 'exuser',
            'password': '0001',
            'database': 'baseball_stat',
            'auth_plugin': 'mysql_native_password'
        }

        # MySQL 연결
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # 테이블 이름 생성
        table_name = f"regular_{year}_{position}"

        if position == "hitter":
            po = "ht"
        elif position == "pitcher":
            po = "pt"
        elif position == "defender":
            po = "df"
        elif position == "runner":
            po = "run"
        else:
            print("None position")

        # 선수 정보 검색 쿼리 실행
        cursor.execute(f"SELECT * FROM {table_name} WHERE {po}_Playername=%s", (player_name,))
        player_info = cursor.fetchone()

        # 연결 및 커서 닫기
        cursor.close()
        conn.close()

        # 결과를 딕셔너리 형태로 반환
        if player_info:
            if po == "ht":
                return {
                    '선수 이름': player_info[0],
                    '팀': player_info[1],
                    '평균 타율': player_info[2],
                    '경기': player_info[3],
                    '타석': player_info[4],
                    '타수': player_info[5],
                    '득점': player_info[6],
                    '안타': player_info[7],
                    '2루타': player_info[8],
                    '3루타': player_info[9],
                    '홈런': player_info[10],
                    '루타': player_info[11],
                    '타점': player_info[12],
                    '희생번트': player_info[13],
                    '희생플라이': player_info[14]
                }
            elif po == "pt":
                return {
                    '선수 이름': player_info[0],
                    '팀': player_info[1],
                    '평균 자책점': player_info[2],
                    '경기': player_info[3],
                    '완투': player_info[4],
                    '완봉': player_info[5],
                    '승리': player_info[6],
                    '패배': player_info[7],
                    '세이브': player_info[8],
                    '홀드': player_info[9],
                    '승률': player_info[10],
                    '타자수': player_info[11],
                    '이닝': player_info[12],
                    '피안타': player_info[13],
                    '홈런': player_info[14],
                    '볼넷': player_info[15],
                    '사구': player_info[16],
                    '삼진': player_info[17],
                    '실점': player_info[18],
                    '자책점': player_info[19]
                }
            elif po == "df":
                return {
                    '선수 이름': player_info[0],
                    '팀': player_info[1],
                    '포지션': player_info[2],
                    '경기': player_info[3],
                    '선발경기': player_info[4],
                    '수비이닝': player_info[5],
                    '실책': player_info[6],
                    '견제사': player_info[7],
                    '풋아웃': player_info[8],
                    '어시스트': player_info[9],
                    '병살': player_info[10],
                    '수비율': player_info[11],
                    '포일': player_info[12],
                    '도루허용': player_info[13],
                    '도루실패': player_info[14],
                    '도루저지율': player_info[15]
                }
            elif po == "run":
                return {
                    '선수 이름': player_info[0],
                    '팀': player_info[1],
                    '경기': player_info[2],
                    '도루시도': player_info[3],
                    '도루허용': player_info[4],
                    '도루실패': player_info[5],
                    '도루성공률': player_info[6],
                    '주루사': player_info[7],
                    '견제사': player_info[8]
                }
        return None

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
