import sys, os, time
import typing
from interface import Ui_MainWindow
from deepface import DeepFace
import PyQt5
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class MyFunc(QMainWindow):
      def __init__(self, parent: typing.Optional[QWidget] = ..., flags: typing.Union[Qt.WindowFlags, Qt.WindowType] = ...) -> None:
          super().__init__()
          self.ui = Ui_MainWindow()
          self.ui.setupUi(self)
          ##########################
          self.setWindowTitle('Face Scanner')


          # установка иконки приложения
          pixmap = QPixmap('icon.png')
          icon = QIcon(pixmap)
          self.setWindowIcon(icon)


          # запуск всех нужных методов
          self.load_combo()
          self.load_font()
          self.ui.image_1.setText(None)
          self.ui.image_2.setText(None)
          self.is_image = False
          self.is_image_2 = False

          # Обработчики клика на кнопку
          self.ui.btn_image1.clicked.connect(self.add_image_1)
          self.ui.btn_image2.clicked.connect(self.add_image_2)
          self.ui.brn_final.clicked.connect(lambda: self.message_box("Информация", "При первом анализе загрузка может потребовать времени!\n Нажмите 'ОК' и загрузка начнётся"))
          self.ui.brn_final.clicked.connect(self.review)

          # Запуск метода при старте(информация)
          self.message_box_start()

          # Обработка меню
          self.action_exit = QAction(self)
          self.ui.menu_2.addAction(self.action_exit)
          self.action_exit.setText('Выйти')
          self.action_exit.triggered.connect(self.exit_app)
          self.ui.action.triggered.connect(self.info)

          # Путь к изображениям для дальнейшего удаления
          self.image_path_1 = 'image_review_1.png'
          self.image_path_2 = 'image_review_2.png'
          # Выравнивание текста по центру

          self.ui.label_main_name.setAlignment(Qt.AlignCenter)
          
          







      # Загружаем шрифт в виджеты
      def load_font(self):
         font_id = QFontDatabase.addApplicationFont("font.otf")
         font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
         font = QFont(font_family)
         # Установка шрифта
         font.setPointSize(11)
         self.ui.brn_final.setFont(font)
         self.ui.btn_image1.setFont(font)
         font.setPointSize(9)
         self.ui.combo_choose.setFont(font)
         font.setPointSize(11)
         self.ui.btn_image2.setFont(font)
         font.setPointSize(16)
         self.ui.label_main_name.setFont(font)





      # Загружаем разделы в комбо бокс
      def load_combo(self):
           self.ui.combo_choose.addItem('Похожи ли эти фото')
           self.ui.combo_choose.addItem('Проверка возраста')
           self.ui.combo_choose.addItem('Проверка рассы')
           self.ui.combo_choose.addItem('Проверка гендера')
           self.ui.combo_choose.addItem('Проверка эмоций')
      # обработчик сигнала клика на кнопку(добавление изображения)
      def add_image_1(self):
        file_name, _ = QFileDialog.getOpenFileName(None, "Выбрать изображение", "", "Images (*.png *.xpm *.jpg)")
        if file_name:
            self.is_image = True
        else:
            return self.message_box('Ошибка', 'Вы не выбрали файл!')
        pixmap = QPixmap(file_name)

        image_review_1 = pixmap.toImage()
        self.ui.image_1.setPixmap(pixmap)
        self.ui.image_1.setScaledContents(True)

        image_review_1.save("image_review_1.png")
      # обработчик сигнала клика на кнопку(добавление изображения)
      def add_image_2(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Выбрать файл", "", "Image files (*.png *.xpm *.jpg)")
        pixmap = QPixmap(file_name)

        image_review_2 = pixmap.toImage()
        self.ui.image_2.setPixmap(pixmap)
        self.ui.image_2.setScaledContents(True)

        image_review_2.save("image_review_2.png")
        self.is_image_2 = True

      # Основной метод для анализа
      def review(self):
          current_item = self.ui.combo_choose.currentText()
          if current_item == 'Похожи ли эти фото':
            if self.is_image and self.is_image_2:               
              self.face_verify()
            else:
               self.message_box('Ошибка', 'Загрузите фото!')
          elif current_item == 'Проверка возраста' or current_item == 'Проверка рассы' or current_item == 'Проверка гендера' or 'Проверка эмоций':
            if self.is_image:
              self.face_analyze()
            else:
               self.message_box('Ошибка', 'Загрузите фото в первую ячейку!')

             
               
          
      

      # Гибкий метод для выведения сообщения об ошибке и тд.
      def message_box(self, title, text):
        res = QMessageBox()
        res.setFixedSize(200, 150)
        res.setWindowTitle(title)
        res.setText(text)
        res.setIcon(QMessageBox.Warning)
        res.exec_()





      # Проверка схожести фото
      def face_verify(self):
        try:
            result_dict = DeepFace.verify(img1_path="image_review_1.png", img2_path="image_review_2.png")
            
            if result_dict.get('verified'):
                self.ui.label_main_name.setText('Одинаковые люди')
                
            else:
                self.ui.label_main_name.setText('Разные люди')
            return result_dict
        except Exception as _ex:
            return _ex
        
      # Проверка возраста, рассы, гендера и эмоций
      def face_analyze(self):
        current_item = self.ui.combo_choose.currentText()

        # Проверка возраста
        if current_item == 'Проверка возраста':
          result = DeepFace.analyze(img_path='image_review_1.png', actions=['age'])
          age = result[0]["age"]
          self.ui.label_main_name.setText('Возраст по фото: ' + str(age) + ' лет(года)')
          return result
        
        # Проверка рассы
        elif current_item == 'Проверка рассы':
          result = DeepFace.analyze(img_path='image_review_1.png', actions=['race'])
          if isinstance(result, list):
            race = result[0]["dominant_race"]
          else:
            race = result["dominant_race"]
          races_dict = {'asian': 'Азиатская',
                      'indian': 'Индийская',
                      'black': 'Афроамериканская',
                      'white': 'Европейская',
                      'middle eastern': 'Ближневосточная',
                      'latino hispanic': 'Латиноамериканская'}
          race_ru = races_dict.get(race, race)
          self.ui.label_main_name.setText(f"Раса: {race_ru}")
          return result
        
        # Проверка гендера
        elif current_item == 'Проверка гендера':
          result = DeepFace.analyze(img_path='image_review_1.png', actions=['gender'])
          if isinstance(result, list):
            race = result[0]["dominant_gender"]
          else:
            race = result["dominant_gender"]
          if race == 'Woman':
             gender_ru = 'Женский'
          elif race == 'Man':
             gender_ru = 'Мужской'
          self.ui.label_main_name.setText('Гендер: '+ gender_ru)
          return result
        
        # Проверка эмоций
        elif current_item == 'Проверка эмоций':
           result = DeepFace.analyze(img_path='image_review_1.png', actions=['emotion'])
           if isinstance(result, list):
            emotions = result[0]["emotion"]
           else:
            emotions = result["emotion"]
           emotions_ru = {"angry": "Злость", "disgust": "Отвращение", "fear": "Страх", "happy": "Счастье", "neutral": "Нейтральность", "sad": "Грусть", "surprise": "Удивление"}
           emotion_en = max(emotions, key=emotions.get) # выбираем наиболее вероятную эмоцию на английском языке
           emotion_ru = emotions_ru[emotion_en] # переводим на русский язык
           self.ui.label_main_name.setText('Эмоция: '+ emotion_ru)
           return result
        

      # Всплывающее сообщение при старте программы
      def message_box_start(self):
        res = QMessageBox()
        res.setFixedSize(600, 450)
        res.setWindowTitle('Отказано!')
        res.setText(f"Перед использванием программы, прочтите данные пункты: \n • Изображения должны быть качественными!\n• Программа определяет точные результаты при правильном её использовании\n• Убедитесь, что знаете как работает программа!\n• Используйте только первую ячейку фото(левую) для распознавания только одного фото!")
        res.setIcon(QMessageBox.Information)
        res.exec_()

      # Выход на клик по menu
      def exit_app(self):
         QApplication.quit()


      # Переопределение метода при закрытии программы для удаления фото, которые были сохранены
      def closeEvent(self,event):
         # Удаление сохраненных приложением файлов
         if self.is_image:
          os.remove(self.image_path_1)
         if self.is_image_2:
          os.remove(self.image_path_2)

         event.accept()


      # Обработчик клика по меню-информация
      def info(self):
         self.message_box_start()

      











# Основной запуск приложения
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyFunc()
    window.show()
    sys.exit(app.exec_())
