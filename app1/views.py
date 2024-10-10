from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import pandas as pd
from sklearn.preprocessing import LabelEncoder

def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1!=pass2:
            return HttpResponse("Your password and confrom password are not Same!!")
        else:

            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')
        



    return render (request,'signup.html')

def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('predict_diabetes')
        else:
            return HttpResponse ("Username or Password is incorrect!!!")

    return render (request,'login.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def predict_diabetes(request):
    if request.method == 'POST':
        pregnancies = request.POST.get('pregnancies')
        glucose = request.POST.get('glucose')
        bloodpressure = request.POST.get('bloodpressure')
        skinthickness = request.POST.get('skinthickness')
        insulin = request.POST.get('insulin')
        bmi = request.POST.get('bmi')
        diabetes_pedigree_function = request.POST.get('diabetes_pedigree_function')
        age = request.POST.get('age')

        if all([pregnancies, glucose, bloodpressure, skinthickness, insulin, bmi, diabetes_pedigree_function, age]):
            try:
                pregnancies = int(pregnancies)
                glucose = float(glucose)
                bloodpressure = float(bloodpressure)
                skinthickness = float(skinthickness)
                insulin = float(insulin)
                bmi = float(bmi)
                diabetes_pedigree_function = float(diabetes_pedigree_function)
                age = float(age)

                # Load the CSV data if needed
                path = "C:\\Users\\Shashank\\Desktop\\Diabetes\\diabetes.csv"
                data = pd.read_csv(path)

                le = LabelEncoder()
                data['outcome'] = le.fit_transform(data['outcome'])
                inputs = data.drop('outcome', axis=1)
                output = data['outcome']

                # Split data into training and testing sets (70% train, 30% test)
                X_train, X_test, y_train, y_test = train_test_split(inputs, output, test_size=0.3, random_state=42)

                # Initialize and fit the model
                model = DecisionTreeClassifier()
                model.fit(X_train, y_train)

                # Make predictions on the test set
                predictions = model.predict(X_test)

                # Calculate accuracy
                accuracy = accuracy_score(y_test, predictions)
                print(f"Accuracy of the model: {accuracy * 100:.2f}%")

                res = model.predict([[pregnancies, glucose, bloodpressure, skinthickness, insulin, bmi, diabetes_pedigree_function, age]])

                if res[0] == 1:
                    result = "Diabetes is positive in the patient..!!! Please take care of your health"
                else:
                    result = "Diabetes is negative in the patient...!!! Best of luck Good health leads to happy life"

                return render(request, 'prediction_result.html', {'result': result})
            except ValueError:
                messages.error(request, 'Invalid input. Please enter valid numbers.')
                return render(request, 'predict_diabetes.html')
        else:
            messages.error(request, 'Please fill in all the fields.')
            return render(request, 'predict_diabetes.html')
    else:
        return render(request, 'predict_diabetes.html')