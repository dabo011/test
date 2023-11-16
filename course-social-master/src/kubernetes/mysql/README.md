kubectl apply -f mysql-pvc.yaml
kubectl apply -f mysql-deployment.yaml

kubectl run -it --rm --image=mysql:5.6 --restart=Never mysql-client -- mysql -h mysql -ppassword

kubectl port-forward svc/mysql 3306:3306