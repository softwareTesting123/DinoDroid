# DinoDroid Evaluation Results

## 3 times coverage results

3 times Coverage.xlsx

## 3 times crash results

3 times Crash.xlsx

## 3 times Crash pairwise comparison

3 times Crash pairwise comparison.xlsx

## SYstem level Crash Filter

DinoDroid disables system level crashes by omitting crash with below logs.

(1) android.app.ActivityThread.handleReceiver

(2) at android.app.ActivityThread.performLaunchActivity

(3) at android.app.ActivityThread.handleServiceArgs

(4) android.app.ActivityThread.performResumeActivity

## Dataset

64 Apps Dataset is at https://drive.google.com/file/d/18CiCNq04uKsKUqjKialc15OFDVE0JRa_/view?usp=sharing

## Other tools setting:

Monkey:
timeout 1h adb -s emulator-5554 shell monkey -p "$packageName" -v --throttle 200 --ignore-crashes --ignore-timeouts --ignore-security-exceptions --bugreport 1000000 > monkey2/"$(basename "$f")"

Sapienz:
timeout 1h python /SPACE/Sapienz-unChanged/main.py "$f">sapienze/"$(basename "$f")"

Stoat:
timeout 1h ruby /SPACE/stoat/Stoat-master/Stoat/bin/run_stoat_testing.rb --model_time 0.4h --mcmc_time 0.6h --app_dir "$f" --avd_name testAVD --avd_port 5554 --stoat_port 2000 --project_type ant>stoat/"$(basename "$f")

Q-testing:
timeout 1h /SPACE/Q-testing/OneDrive-2021-04-08/q-testing-wgx-publish-pyinstaller/main -r /SPACE/Q-testing/OneDrive-2021-04-08/q-testing-wgx-publish-pyinstaller/CONF.txt

## logs:

Monkey:
https://drive.google.com/file/d/1Kkv5DYZX7gr_witGZR-e5Mjam7ccac-v/view?usp=sharing

Sapienz:
https://drive.google.com/file/d/1Pt1ROyZwjlaXrz8WKGzTeipb0Ts4T_su/view?usp=sharing

Stoat:
https://drive.google.com/file/d/1_5LNGd-kdHHeTRllX5Jd63Y9Ncav4qIn/view?usp=sharing

QBE:
https://drive.google.com/file/d/1026EdjzBUXWIvyxO2C6qQuEa81fLCTAs/view?usp=sharing

Q-testing:
https://drive.google.com/file/d/1TsSocRHq38UtLr_cxICe7gr6imkLQ5Xj/view?usp=sharing

DinoDroid:
https://drive.google.com/file/d/1QAEJaBm6dbJ65ehMyFpOZ6NCYzF-ured/view?usp=sharing     (log)
https://drive.google.com/file/d/1Ek25TnMTP3n2mmtwwY0ap-wh3Xgv8Em-/view?usp=sharing    (dataset and model)
 
Other backup:
https://drive.google.com/file/d/1pOyaTLdSGR90IPSL_EumWlfFfxK543c6/view?usp=sharing