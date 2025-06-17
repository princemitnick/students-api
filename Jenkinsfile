pipeline {
  agent any

  environment {
    IMAGE_NAME = "students-api"
    TAG = "latest"
  }

  stages {
    stage('Checkout') {
      steps {
        git branch: 'main', url: 'https://github.com/princemitnick/students-api.git'
      }
    }

    stage('Docker Build') {
      steps {
        sh 'docker build -t ${IMAGE_NAME}:${TAG} .'
      }
    }

    /*stage('Run Pytest') {
      steps {
        sh 'docker run --rm ${IMAGE_NAME}:${TAG} pytest tests'
      }
    }*/

    stage('Trivy Scan') {
      steps {
        sh 'docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy image ${IMAGE_NAME}:${TAG}'
      }
    }

    /*stage('OWASP ZAP') {
      steps {
        sh '''
          docker run -u root -v $(pwd):/zap/wrk/:rw -t owasp/zap2docker-stable zap-baseline.py \
            -t http://host.docker.internal:8000 \
            -r zap_report.html || true
        '''
      }
    }*/

    stage('Deploy to Minikube') {
      steps {
        sh 'kubectl apply -f k8s/deployment.yaml'
        sh 'kubectl apply -f k8s/service.yaml'
      }
    }
  }
}