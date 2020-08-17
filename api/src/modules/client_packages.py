import pymysql.cursors

connection = pymysql.connect(host='127.0.0.1',
                             port=int('3306'),
                             user='root',
                             password='12233445',
                             db='bi2ai',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)


def get_client_packages():
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM bi2ai.deployments AS dep " \
                  "INNER JOIN bi2ai.packages AS pack ON pack.package_id = dep.package_id " \
                  "INNER JOIN bi2ai.users AS users ON users.user_id = dep.user_id " \
                  "WHERE dep.user_id = %s"
            cursor.execute(sql, (input("Please enter user_id: ")))
            result = cursor.fetchone()
            if result is None:
                print("Failed: No such user in Deployments table.")
            else:
                print(result)
    finally:
        connection.close()


def set_client_packages():
    try:
        with connection.cursor() as cursor:
            sql = "SELECT organization_id FROM bi2ai.deployments WHERE organization_id = %s"
            organization_id = input("Please enter organization_id: ")
            cursor.execute(sql, organization_id)
            result = cursor.fetchone()
            if result is None:
                print("Failed: No such organization_id in Organization table.")
            else:
                sql = "SELECT user_id FROM bi2ai.users WHERE user_id = %s"
                user_id = input("Please enter user_id: ")
                cursor.execute(sql, user_id)
                result = cursor.fetchone()
                if result is None:
                    print("Failed: No such user_id in Users table.")
                else:
                    sql = "SELECT package_id FROM bi2ai.packages WHERE package_id = %s"
                    package_id = input("Please enter package_id: ")
                    cursor.execute(sql, package_id)
                    result = cursor.fetchone()
                    if result is None:
                        print("Failed: No such package_id in Packages table.")
                    else:
                        sql = "INSERT INTO `deployments` (`organization_id`,`user_id`, `package_id`) VALUES (%s,%s,%s) "
                        print("Success. Your data have been added.")
                        cursor.execute(sql, (organization_id, user_id, package_id))
        connection.commit()
    finally:
        connection.close()


def del_client_packages():
    try:
        with connection.cursor() as cursor:
            sql = "SELECT user_id FROM bi2ai.deployments WHERE user_id = %s"
            user_id = input("Please enter user_id that you want to delete form Deployments: ")
            cursor.execute(sql, user_id)
            result = cursor.fetchone()
            if result is None:
                print("Failed: No such user_id in Deployments table.")
            else:
                sql = "SELECT package_id FROM bi2ai.deployments WHERE package_id = %s AND user_id = %s"
                package_id = input("Please enter package_id that you want to delete form Deployments: ")
                cursor.execute(sql, (package_id, user_id))
                result = cursor.fetchone()
                if result is None:
                    print("Failed: No such package_id in Deployments table.")
                else:
                    sql = "DELETE FROM bi2ai.deployments WHERE user_id = %s AND package_id = %s"
                    print("Success. Your data have been deleted.")
                    cursor.execute(sql, (user_id, package_id))
        connection.commit()
    finally:
        connection.close()
