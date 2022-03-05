pipeline {
  agent any
  stages {
    stage('Build Docker image') {
      steps {
        script {
            docker build --tag jeec_brain:latest .
        }
      }
    }
    stage('Deploy Production') {
      steps {
        script {
            if( "${env.BRANCH_NAME}" == "master" ) {
                sh(returnStdout: true, script: '''#!/bin/bash
                    if [ "$(docker ps -q -f name=jeec_brain)" ];then
                    echo "Stopping old jeec_brain Docker container..."
                    docker stop jeec_brain
                    docker rm jeec_brain
                    echo "Old jeec_brain Docker container stopped!"
                    fi

                    echo "Starting new Docker container..."
                    docker run -p 8081:8081 --name jeec_brain -d jeec_brain:latest
                    echo "Docker container started!"
                '''.stripIndent())
            }
           
        }
      }
    }
  
  }
}
