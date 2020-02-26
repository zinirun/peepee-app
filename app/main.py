import cv2
from sklearn.cluster import KMeans
from flask import Flask, url_for, render_template, request, redirect

ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png', 'gif', 'bmp', 'JPG', 'JPEG', 'PNG', 'GIF', 'BMP'])
app = Flask(__name__)

# 업로드 HTML 렌더링
@app.route('/')
def upload():
    return render_template('index.html')


# 파일 업로드 처리
@app.route('/fileUpload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        #확장자 이미지파일인 경우
        if file and allowed_file(file.filename):
            file.save('uploads/' + 'image.' + 'jpg')
            return redirect(url_for('run_anal'))
        #확장자 이미지파일 아닐 경우
        return render_template('index.html', data="이미지 파일만 업로드하세요.")


#파일 확장자 검사
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


#CV2 처리
def load_n_crop():
    img_bgr = cv2.imread("uploads/image.jpg", cv2.IMREAD_COLOR)
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    # crop the image
    x, y, channel = img_bgr.shape
    x = int(x / 2)  # width
    y = int(y / 2)  # height
    dst = img_rgb.copy()
    dst = dst[(x - 50):(x + 50), (y - 50):(y + 50)]

    # use K-mean algorithm to find mean value of colors
    new_rgb = dst.reshape((dst.shape[0] * dst.shape[1], 3))
    clt = KMeans(n_clusters=1)
    clt.fit(new_rgb)

    col = clt.cluster_centers_.astype("uint8").flatten().tolist()
    return col


#rgb에 따른 소변유형 분류
def calc_type(color):
    r, g, b = color
    result = 0
    if r >= 200 and r <= 255:
        if g >= 200 and g <= 225 and b >= 200 and b <= 225:
            result = 1
        elif g >= 226 and g <= 240 and b >= 160 and b <= 199:
            result = 2
        elif g >= 180 and g <= 199 and b >= 100 and b <= 159:
            result = 3
        elif g >= 180 and g <= 220 and b >= 70 and b <= 100:
            result = 4
        elif g >= 180 and g <= 220 and b >= 40 and b < 70:
            result = 5
        elif g >= 120 and g <= 160 and b >= 100 and b <= 140:
            result = 7
        elif g >= 150 and g <= 190 and b >= 100 and b <= 130:
            result = 8
    elif r >= 150 and r <= 199:
        if g >= 140 and g <= 180 and b >= 100 and b <= 140:
            result = 6
        elif g >= 170 and g <= 200 and b >= 120 and b <= 150:
            result = 9
    elif r >= 100 and r <= 150:
        if g >= 90 and g <= 140 and b >= 80 and b <= 130:
            result = 1
        elif g > 113 and g <= 140 and b >= 0 and b <= 40:
            result = 2
        elif g >= 60 and g <= 113 and b >= 0 and b <= 40:
            result = 3
        elif g >= 90 and g <= 130 and b >= 40 and b <= 90:
            result = 4
        elif g >= 90 and g <= 130 and b >= 20 and b < 40:
            result = 5
    return result


#분석 실행
@app.route('/mod')
def run_anal():
    result = calc_type(load_n_crop())
    return render_template('result.html', peeValue=result)


if __name__ == '__main__':
    # 서버 실행
    app.run(host='0.0.0.0', debug=True, port=80)