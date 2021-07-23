# FingerBeam
**2021_SangsaengProject**

![result_img](https://user-images.githubusercontent.com/76740863/126743176-06740522-57ee-4919-83f1-117dac18cf54.GIF)

### FingerBeam팀 (2021.03.23 ~ 2021.05.30)

공중에서 필기, 저장 기능을 제공하는 시스템

# Role

|                            이름                             |              역할              |                           책임                            |
| :---------------------------------------------------------: | :----------------------------: | :-------------------------------------------------------: |
|   [leemijung(이미정)](https://github.com/leemijung)     |       Team Leader 👑        |                전체적인 프로젝트 관리 담당                |
|   [youngseo0526(김영서)](https://github.com/youngseo0526)   |        Front-end Coder         |               Client Side 기능 구현 및 관리               |
|   [An-Byeong-Seon(안병선)](https://github.com/An-Byeong-Seon)   |        Back-end Coder         |               Server Side 기능 구현 및 관리               |
|   [201910835(정은혜)](https://github.com/201910835)   |        Front-end Coder         |            Client Side 기능 구현 및 관리                  |
|   [00ssum(조수민)](https://github.com/00ssum)   |        Back-end Coder         |              Server Side 기능 구현 및 관리                |

-------------------

**1. 메인 기능**

- **문서 업로드** : 필기하고자 하는 pdf문서를 업로드

- **필기** : 필기시작/필기중단/페이지이동

- **로컬 저장** : 필기가 종료된 pdf문서를 다시 로컬에 

-------------------

**2.개발 도구**

- **pychram** : OpenCV 구동 및 Python 코드 구현

- **Kakao Oven** : 구체적인 UI 스케치

-------------------

**3. 프로젝트 환경 구현**

#### Install opencv

#### pip install (최초 1회 실행)

```
pip install opencv-python
```

#### Code

```
import cv2
```

------------------------

**4. 실행 화면**

<br>

- 커버 화면

핑거빔 소개 & 시작 버튼을 눌러 업로드 화면으로 넘어감

![1](https://user-images.githubusercontent.com/76740863/123056193-9e603500-d441-11eb-8438-586434d218bc.jpg)

<br>

- 업로드 화면

내 pc에서 필기하고자 하는 문서 업로드 & pdf 형식으로 변환 진행

![2](https://user-images.githubusercontent.com/76740863/123056201-9f916200-d441-11eb-9fee-e3e374bad417.jpg)

<br>

- 메인 화면

필기시작 버튼을 눌러 필기 진행화면으로 넘어감

![3](https://user-images.githubusercontent.com/76740863/123056202-9f916200-d441-11eb-9ff0-312faa09925c.jpg)

<br>

- 필기 진행화면

문서의 페이지가 나타나고, 필기를 진행 & 'space bar' 필기 전체 삭제 & 'v' 필기 on/off

![4](https://user-images.githubusercontent.com/76740863/123056203-a029f880-d441-11eb-8d78-68e165a00213.jpg)

<br>

- 저장 화면

'예' 버튼을 눌러 내 pc로 문서 다운로드 가능

![5](https://user-images.githubusercontent.com/76740863/123056208-a15b2580-d441-11eb-8e6e-61004abe624b.jpg)

<br>

- 결과 pdf 도출화면

![6](https://user-images.githubusercontent.com/76740863/123056789-3827e200-d442-11eb-924d-cbc3dd1ed545.jpg)


