pipeline {
  agent any

  environment {
    DOTENV_FILE_ID = credentials('brain-environment-variables')
  }

  stages {
    stage('Build Docker image') {
      steps {
        sh 'cp ${DOTENV_FILE_ID} .'
        sh 'docker build --tag jeec_brain:latest .'
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
                if [ "$(docker ps -q -f name=jeec_brain)" ];then
                echo "Stopping old jeec_brain Docker container..."
                docker stop jeec_brain
                docker rm jeec_brain
                echo "Old jeec_brain Docker container stopped!"
                fi

                echo "Starting new Docker container..."
                docker run -p 8081:8081 --name jeec_brain -d jeec_brain:latest
                echo "Docker container started!"
            '''
        }
      }
    }
  }
}
