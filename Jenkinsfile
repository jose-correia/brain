pipeline {
  agent any

  environment {
    DOTENV_FILE_ID = credentials('brain-environment-variables')
  }

  stages {
    stage('Build Docker image') {
      steps {
        sh 'cp -n ${DOTENV_FILE_ID} .'
        sh 'docker build --tag jeec_brain:latest .'
      }
    }

    stage('Migrate Database') {
      when {
        beforeInput true
        branch 'master'
      }

      input {
        message "Run database migration?"
      }

      steps {
        script {
            sh '''
                echo "Starting database migration..."
                docker-compose up db_migration
                echo "Database migrated successfuly!!"
            '''
        }
      }
    }

    stage('Deploy Production') {
      when {
        beforeInput true
        branch 'master'
      }

      input {
        message "Deploy to production?"
      }

      steps {
        script {
            sh '''
                if [ "$(docker ps -q -a -f name=jeec_brain)" ];then
                echo "Stopping old jeec_brain Docker container..."
                docker stop jeec_brain
                docker rm jeec_brain
                echo "Old jeec_brain Docker container stopped!"
                fi

                echo "Starting new Docker container..."
                docker-compose up -d jeec_brain
                echo "Docker container started!"
            '''
        }
      }
    }
  }
}
