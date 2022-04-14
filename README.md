# XDU 录直播应用
## "公开"API
### 获取某个课程相关的信息
- http://newesxidian.chaoxing.com/live/listSignleCourse
- POST
    - fid=16820
    - liveId=10000742

### 获取某个学生某个学期的某一周的课程
- http://newesxidian.chaoxing.com/frontLive/listStudentCourseLivePage
- GET
    - fid=16820
    - userId=78536002
    - week=2
    - termYear=2020
    - termId=1
    - type=1

### 获取直播地址
- http://newesxidian.chaoxing.com/live/getViewUrlNoCourseLive
- GET/POST
    - deviceCode=004381
        - 硬件码
    - status=1
    - fid=16820
- example

### 获取录播地址
- http://newesxidian.chaoxing.com/live/getViewUrlNoCourseLive
- GET/POST
    - deviceCode=004381
    - status=2
    - fid=16820
    - startTime: 2020-08-31 20:08:56.0
    - endTime: 2020-08-31 21:09:00.0
- startTime和endTime之间需要包含目标时间段
