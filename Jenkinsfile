pipeline {
  agent any

  environment {
    DOTENV_FILE_ID = credentials('brain-environment-variables')
  }

  stages {
    stage('Build Docker image') {
      steps {
        sh 'cp -n ${DOTENV_FILE_ID} .'
        sh 'docker-compose build'
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
                docker-compose up
                echo "Docker container started!"
            '''
        }
      }
    }
  }
}
