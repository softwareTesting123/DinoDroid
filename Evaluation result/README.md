# DinoDroid Evaluation Results

## 3 times coverage results

3 times Coverage.xlsx

## 3 times crash results

3 times Crash.xlsx

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

## logs:

Monkey:


Sapienz:


Stoat:


QBE:

DinoDroid:

