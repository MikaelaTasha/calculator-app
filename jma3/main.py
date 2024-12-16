import flet as ft
import json
import requests
from datetime import datetime, timedelta

def main(page: ft.Page):
    page.spacing = 0
    page.padding = 0

    # Load the JSON data from the file
    with open("jma3/areas.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    # Define the prefecture names mapping
    prefecture_names = {
        "010000": "北海道",
        "011000": "北海道（札幌）",
        "012000": "北海道（函館）",
        "013000": "北海道（旭川）",
        "014030": "北海道（室蘭）",
        "014100": "北海道（帯広）",
        "015000": "北海道（釧路）",
        "016000": "北海道（北見）",
        "017000": "北海道（札幌）",
        "020000": "青森県",
        "030000": "岩手県",
        "040000": "宮城県",
        "050000": "秋田県",
        "060000": "山形県",
        "070000": "福島県",
        "080000": "茨城県",
        "090000": "栃木県",
        "100000": "群馬県",
        "110000": "埼玉県",
        "120000": "千葉県",
        "130000": "東京都",
        "140000": "神奈川県",
        "150000": "新潟県",
        "160000": "富山県",
        "170000": "石川県",
        "180000": "福井県",
        "190000": "山梨県",
        "200000": "長野県",
        "210000": "岐阜県",
        "220000": "静岡県",
        "230000": "愛知県",
        "240000": "三重県",
        "250000": "滋賀県",
        "260000": "京都府",
        "270000": "大阪府",
        "280000": "兵庫県",
        "290000": "奈良県",
        "300000": "和歌山県",
        "310000": "鳥取県",
        "320000": "島根県",
        "330000": "岡山県",
        "340000": "広島県",
        "350000": "山口県",
        "360000": "徳島県",
        "370000": "香川県",
        "380000": "愛媛県",
        "390000": "高知県",
        "400000": "福岡県",
        "410000": "佐賀県",
        "420000": "長崎県",
        "430000": "熊本県",
        "440000": "大分県",
        "450000": "宮崎県",
        "460000": "鹿児島県",
        "470000": "沖縄県",
    }

    # State to hold selected region's weather info
    selected_region_info = ft.Ref[ft.Text]()
    selected_date = ft.Ref[ft.DatePicker]()

    def create_expansion_tile(center_id, center_data):
        # Create a ListTile for each child
        children = [
            ft.ListTile(
                title=ft.Text(prefecture_names.get(child, "Unknown")),
                on_click=lambda e, child_id=child: show_weather_info(child_id)
            ) for child in center_data['children']
        ]
        return ft.ExpansionTile(
            title=ft.Text(center_data["name"]),
            subtitle=ft.Text(center_data["enName"]),
            leading=ft.Icon(ft.icons.LOCATION_ON),
            controls=children,
        )

    def show_weather_info(area_code):
        # Fetch weather info from JMA API
        region_name = prefecture_names.get(area_code, "Unknown Region")
        date = selected_date.current.value
        if date:
            date_str = datetime.strptime(date, "%Y-%m-%d").strftime("%Y%m%d")
        else:
            date_str = datetime.now().strftime("%Y%m%d")

        try:
            response = requests.get(f"https://www.jma.go.jp/bosai/forecast/data/forecast/{area_code}.json")
            response.raise_for_status()
            weather_data = response.json()
            weather_info = f"{region_name} の天気: {weather_data[0]['timeSeries'][0]['areas'][0]['weathers'][0]}, 気温: {weather_data[0]['timeSeries'][2]['areas'][0]['temps'][0]}°C"
        except requests.exceptions.RequestException as e:
            weather_info = f"{region_name} の天気情報を取得できませんでした。エラー: {e}"
        
        selected_region_info.current.value = weather_info
        page.update()

    # Create expansion tiles for each center
    expansion_tiles = [
        create_expansion_tile(center_id, center_data)
        for center_id, center_data in data['centers'].items()
    ]

    # Sidebar
    sidebar = ft.Container(
        content=ft.Column(controls=expansion_tiles, width=300),
        bgcolor=ft.colors.BLUE_GREY,
    )

    # Main content area
    main_content = ft.Column(
        controls=[
            ft.Text("地域を選択してください", ref=selected_region_info),
            ft.DatePicker(ref=selected_date)
        ],
        alignment=ft.MainAxisAlignment.START,
    )

    # AppBar
    app_bar = ft.AppBar(
        title=ft.Row(
            [ft.Icon(ft.icons.WB_SUNNY), ft.Text("天気予報")],
            alignment=ft.MainAxisAlignment.START,
        ),
        bgcolor=ft.colors.PURPLE,
    )

    # Layout
    page.add(
        app_bar,
        ft.Row(
            controls=[sidebar, main_content],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.START,
        ),
    )

ft.app(main)