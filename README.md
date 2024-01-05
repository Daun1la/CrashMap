# CrashMap
---
## Getting Started

1.  Install libraries:

    ```shell
    pip install psycopg2-binary
    pip install flask
    pip install pandas
    pip install numpy
    pip install folium 
    ```

### Database Configuration

1.  If you want to put the collected data into the database, then there is a separate section for this which needs to be commented out
1.  Create a config file in the same folder where you write your data, also you can write path to your folder with data there.

     ```shell
    host = "your host (127.0.0.1 as default)"
    user = "your name (postgres)"
    password = "your password"
    db_name ="your db name"
    folder_path = 'your path to folder'
    ```
### HTTP tunneling
If you want to make your web page accessible to any user, you can use the ngrok utility. [Ngrok](https://ngrok.com/) creates a tunnel between your computer and a remote server and provides access to it from a unique domain (address), which it generates itself.

[Instruction](https://habr.com/ru/articles/697620/)
