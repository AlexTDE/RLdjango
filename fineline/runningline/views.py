from django.http import FileResponse, HttpResponse
from django.shortcuts import render
import cv2
import numpy as np
import os

# Функция для создания видео с бегущей строкой
def create_video_opencv(message):
    # Размеры видео (ширина x высота)
    width, height = 100, 100

    # Задаём параметры - видеопоток с частотой 24 кадра в секунду
    out = cv2.VideoWriter("my_video.mp4", cv2.VideoWriter_fourcc(*'mp4v'), 18, (width, height))

    # Создаем кадр с черным фоном
    frame = np.zeros((height, width, 3), dtype=np.uint8)

    # Начальные координаты для бегущей строки
    x, y = width, height // 2

    # Установим параметры шрифта
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    font_thickness = 2
    font_color = (255, 255, 255)  # Белый цвет текста

    # Пройдемся по каждому кадру
    for t in range(60):
        # Очистка кадра
        frame.fill(0)

        # Новые координаты для бегущей строки
        x -= 10  # Скорость бегущей строки

        # Вот тут добавим текст
        cv2.putText(frame, message, (x, y), font, font_scale, font_color, font_thickness)

        # Тут запишем кадр
        out.write(frame)

    # Закроем тут видеопоток
    out.release()

    # Возвращаем путь к файлу
    return "my_video.mp4"

def index(request, text):
    video_path = create_video_opencv(text)
    response = FileResponse(open(video_path, 'rb'))
    response['Content-Disposition'] = f'attachment; filename="{os.path.basename(video_path)}"'
    return response

def base(request):
    return HttpResponse("<h1>Go to http://localhost:8000/runningtext=\"your text\" to create running line<h1>")