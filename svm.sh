cd libsvm-3.12/java/
java svm_train -b 1 -t 0 ../../training ../../trained.model
java svm_predict -b 1 ../../test ../../trained.model ../../answer
cd ../../
