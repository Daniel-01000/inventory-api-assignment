pipeline {
    agent any

    environment {
        IMAGE_NAME = 'inventory-api'
        CONTAINER_NAME = 'inventory-api-jenkins'
        ZIP_NAME = "complete-${new Date().format('yyyy-MM-dd-HH-mm-ss')}.zip"
        DOCKER_CMD = '/usr/local/bin/docker'
        PATH = "/Applications/Docker.app/Contents/Resources/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"
        MONGO_URI = "mongodb+srv://sofoladaniel1_db_user:xcmeXz43R7LqviWW@cluster0.sygoaqi.mongodb.net/?appName=Cluster0"
        DB_NAME = "inventory_db"
        COLLECTION_NAME = "products"
        NEWMAN_CMD = "/Users/ayomidesofola/.nvm/versions/node/v20.19.5/bin/newman"
    }

    stages {
        stage('Clone / Checkout') {
            steps {
                echo 'Using repository checked out by Jenkins job configuration'
            }
        }

        stage('Create README.txt') {
            steps {
                sh '''
                cat > README.txt <<EOF
Inventory Management API

Endpoints:
/                  -> Home
/getAll            -> Returns all products
/getSingleProduct  -> Takes product_id
/addNew            -> Takes ProductID, Name, UnitPrice, StockQuantity, Description
/deleteOne         -> Takes product_id
/startsWith        -> Takes letter
/paginate          -> Takes start_id and end_id
/convert           -> Takes product_id and returns euro price

FastAPI Docs:
http://127.0.0.1:8000/docs
EOF
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                echo $PATH
                which docker-credential-desktop || true
                $DOCKER_CMD build -t $IMAGE_NAME .
                '''
            }
        }

        stage('Run Docker Container in Background') {
            steps {
                sh '''
                $DOCKER_CMD rm -f $CONTAINER_NAME || true
                $DOCKER_CMD run -d \
                  -p 8000:8000 \
                  -e MONGO_URI="$MONGO_URI" \
                  -e DB_NAME="$DB_NAME" \
                  -e COLLECTION_NAME="$COLLECTION_NAME" \
                  --name $CONTAINER_NAME \
                  $IMAGE_NAME
                '''
            }
        }

        stage('Wait for API') {
            steps {
                sh '''
                sleep 10
                curl http://127.0.0.1:8000/
                '''
            }
        }

        stage('Run Newman Tests') {
            steps {
                sh '''
                $NEWMAN_CMD run inventory_api_tests.postman_collection.json
                '''
            }
        }

        stage('Create Final Zip') {
            steps {
                sh '''
                zip -r $ZIP_NAME . -x "venv/*" ".git/*" "__pycache__/*" ".history/*"
                '''
            }
        }
    }

    post {
        always {
            sh '''
            $DOCKER_CMD stop $CONTAINER_NAME || true
            $DOCKER_CMD rm $CONTAINER_NAME || true
            '''
            archiveArtifacts artifacts: 'README.txt, complete-*.zip', fingerprint: true
        }
    }
}