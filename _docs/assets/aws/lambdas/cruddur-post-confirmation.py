import json
import psycopg2

def lambda_handler(event, context):
    user = event['request']['userAttributes']
    try:
        conn = psycopg2.connect(os.getenv('CONNECTION_URL')
        )
        cur = conn.cursor()
        print('user Attributes')

        user_display_name = user['name']
        user_email        = user['email'] 
        user_handle       = user['prefered_username']
        user_cognito_id   = user['sub']

        sql = f"""
         "INSERT INTO users (
            display_name, 
            handle,
            email, 
            cognito_user_id
            ) 
         VALUES(
            {user_display_name},
            {user_handle},
            {user_email},
            {user_cognito_id}
           )"
        """
        cur.execute(sql)
        conn.commit() 

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        
    finally:
        if conn is not None:
            cur.close()
            conn.close()
            print('Database connection closed.')

    return event