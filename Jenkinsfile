pipeline {
  agent any

  environment {
    AUTHOR = "Prin..."
    DOCKER_IMAGE = "princemitnick/students-api"
    VERSION = "1.0.${BUILD_NUMBER}"
    TAG_BUILD = "${DOCKER_IMAGE}:${VERSION}"
    TAG_LATEST = "${DOCKER_IMAGE}:latest"
    KUBECONFIG = "/var/lib/jenkins/.kube/config"
  }

  options {
    timestamps()
  }

  stages {

    stage('Checkout Code') {
      steps {
        git branch: 'feature/cicd-pipeline', url: 'https://github.com/princemitnick/students-api.git'
      }
    }

    stage('Build Docker Image') {
      steps {
        sh '''
          eval $(minikube docker-env)
          docker build -t ${TAG_BUILD} -t ${TAG_LATEST} .
        '''
      }
    }

    stage('Run Pytest') {
      steps {
        sh 'docker run --rm ${TAG_BUILD} pytest tests'
      }
    }

    stage('Trivy Security Scan') {
      steps {
        sh '''
          docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy image ${TAG_BUILD}
        '''
      }
    }

    stage('Push Docker Image to DockerHub') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub-secrets', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
          sh '''
            echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
            docker push ${TAG_BUILD}
            docker push ${TAG_LATEST}
          '''
        }
      }
    }

    stage('Deploy to Minikube') {
      steps {
        sh '''
          export KUBECONFIG=${KUBECONFIG}
          kubectl set image deployment/students-deployment students=${TAG_BUILD} --record || kubectl apply -f k8s/deployment.yaml
          kubectl apply -f k8s/service.yaml
        '''
      }
    }

    stage('OWASP ZAP Scan') {
      steps {
        sh '''
          sleep 10
          API_URL=$(minikube service students-service --url)
          docker run -v $(pwd):/zap/wrk -t ghcr.io/zaproxy/zaproxy:stable zap-baseline.py \
            -t "$API_URL" -r zap_report.html || true
        '''
      }
    }

    stage('Smoke Test') {
      steps {
        sh '''
          API_URL=$(minikube service students-service --url)
          curl --fail "$API_URL/students"
        '''
      }
    }
  }

  post {
    failure {
      echo "Pipeline échoué. À corriger avant de merger dans main."
    }
    success {
      echo "Build OK — prêt pour PR vers main."
    }
  }
}