# CrashMap
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
