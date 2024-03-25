import mysql.connector

def get_team_wl(year, team1=None, team2=None):
    try:
        # MySQL 연결 설정
        conn = mysql.connector.connect(
            user="root",
            password="12345678",
            host="localhost",
            database="baseball_stat",
            auth_plugin='mysql_native_password'
        )

        # 커서 생성
        cursor = conn.cursor()

        # 쿼리 생성
        if team1 and team2:  # 두 팀의 승패표를 비교하는 경우
            query = f"SELECT * FROM regular_team_WL_{year} WHERE `team_name` IN ('{team1}', '{team2}')"
        elif team1:  # 특정 팀의 승패표를 가져오는 경우
            query = f"SELECT * FROM regular_team_WL_{year} WHERE `team_name` = '{team1}'"
        else:  # 전체 팀의 승패표를 가져오는 경우
            query = f"SELECT * FROM regular_team_WL_{year}"

        # 쿼리 실행
        cursor.execute(query)

        # 컬럼 이름 가져오기
        columns = [col[0] for col in cursor.description]

        # 컬럼 이름 출력
        print(columns)

        # 결과 가져오기
        team_wl = cursor.fetchall()

        # 결과 출력
        for wl in team_wl:
            print(wl)

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
