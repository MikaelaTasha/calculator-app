import flet as ft
import json

def main(page: ft.Page):
    page.spacing = 0
    page.padding = 0
    
    # Load the JSON data from the file
    with open("jma2/areas.json", "r", encoding="utf-8") as file:
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

    # A function to create an expansion tile for each center
    def create_expansion_tile(center_id, center_data):
        # Create a ListTile for each child, showing the prefecture name above the ID
        children = [
            ft.ListTile(
                title=ft.Column(
                    [
                        ft.Text(prefecture_names.get(child, "Unknown"), weight=ft.FontWeight.BOLD),  # Prefecture name
                        ft.Text(child)  # Child ID number
                    ]
                )
            ) 
            for child in center_data['children']
        ]
        return ft.ExpansionTile(
            title=ft.Text(center_data["name"]),
            subtitle=ft.Text(center_data["enName"]),
            leading=ft.Icon(ft.icons.LOCATION_ON),  # You can customize the leading icon
            trailing=ft.Icon(ft.icons.ARROW_DROP_DOWN),
            controls=children,
        )

    # Create a list of expansion tiles for each center in the JSON data
    expansion_tiles = []
    for center_id, center_data in data['centers'].items():
        expansion_tiles.append(create_expansion_tile(center_id, center_data))

    # Create the sidebar by using a Column to hold the expansion tiles
    sidebar = ft.Container(
        content=ft.Column(
            controls=expansion_tiles,
            width=300,  # Width of the sidebar
        ),
        bgcolor=ft.colors.BLUE_GREY,  # Sidebar background color
    )

    # Create the main content area, can be empty or have other content
    main_content = ft.Column(
        controls=[ft.Text("Main content goes here...")],
        alignment=ft.MainAxisAlignment.START,
    )

    # Add an AppBar with a sunny icon next to the title
    app_bar = ft.AppBar(
        title=ft.Row(
            [
                ft.Icon(ft.icons.WB_SUNNY),  # Sunny icon
                ft.Text("天気予想"),  # Title of the AppBar
            ],
            alignment=ft.MainAxisAlignment.START,  # Align the title and icon to the left
        ),
        bgcolor=ft.colors.PURPLE,  # Background color for the AppBar
    )

    # Layout the page with a Row: AppBar on top, sidebar on the left, and main content on the right
    page.add(
        app_bar,  # AppBar at the top
        ft.Row(
            controls=[sidebar, main_content],  # Sidebar and main content
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.START,
        ),
    )

ft.app(main)
