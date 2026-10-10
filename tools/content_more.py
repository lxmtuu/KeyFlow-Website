#!/usr/bin/env python3
"""The remaining pages: gallery, guide and download."""
from __future__ import annotations

from sitekit import (ASSETS, CHANGELOG, CHANGELOG_VI, DOTNET, E, FREEPATS, ISSUES, LICENSE,
                     README_EN, README_VI, RELEASES, RELEASE_PAGE, REPO, T, VORTICE, band,
                     callout, carousel, chipcloud, codeblock, cta, dlhero, faq, framed, grid,
                     groups, iconbox, pagehero, picture, pagenav, raw, slider, split, specdl,
                     steps, table)

DOWNLOAD = {"label": T("Download for Windows", "Tải cho Windows"), "href": "download.html",
            "kind": "btn-gold", "icon": "download"}

# Every screenshot the application's CI renders, per language.
STAGE_SHOTS = ["stage-live", "stage-gpu", "stage-gpu-galaxy", "stage-gpu-storm", "background-image"]
UI_SHOTS = ["main-menu", "design-dock", "theme-dock", "language-dock"]
SESSION_SHOTS = ["play-dialog", "practice-dock", "history-dock", "recording-dock", "shortcuts"]


def kbd(*keys: str) -> str:
    return " ".join("<kbd>" + k + "</kbd>" for k in keys)


# ===========================================================================
# Gallery
# ===========================================================================
def build_gallery(doc) -> dict:
    root = doc.root

    presets_k, presets_v = doc.key(T(
        "A preview of two preset comparisons; open the full image to see all fourteen",
        "Bản xem trước hai phép so sánh preset; mở ảnh đầy đủ để xem cả mười bốn"))
    presets_note_k, presets_note_v = doc.key(T(
        "This preview shows two preset comparisons from the CI mosaic: the software renderer and GPU engine draw each look "
        "side by side. The full image covers all fourteen presets, so you can compare pressed-key colour, the horizon, "
        "hollow neon tubes and Fire's cracks. Open the full picture.",
        "Bản xem trước này gồm hai phép so sánh từ ảnh ghép CI: bộ dựng hình phần mềm và engine GPU render mỗi diện "
        "mạo cạnh nhau. Ảnh đầy đủ có cả mười bốn preset để bạn so sánh màu phím đang nhấn, đường chân trời, ống "
        "neon rỗng và vết nứt của Fire. Mở ảnh đầy đủ."))
    presets_html = (
        '<figure class="shot" style="margin:0">'
        '<a href="' + root + 'previews/presets.jpg" target="_blank" rel="noopener">'
        '<picture><source type="image/webp" srcset="' + root + 'previews/webp/presets-teaser.webp">'
        '<img src="' + root + 'previews/presets-teaser.jpg" width="1080" height="720" loading="lazy" '
        'decoding="async" data-i18n-attr="alt=' + presets_k + '" alt="' + presets_v.replace('"', "&quot;") + '">'
        '</picture></a>'
        '<figcaption class="frame-cap" data-i18n="' + presets_note_k + '">' + presets_note_v + "</figcaption>"
        "</figure>"
    )

    video_cap_k, video_cap_v = doc.key(T(
        "The showcase clip at the top of this site: one take of the GPU stage playing a score, recorded by Keyflow.",
        "Đoạn video giới thiệu ở đầu trang: một lượt sân khấu GPU chơi một bản nhạc, do chính Keyflow ghi lại."))
    video_label_k, video_label_v = doc.key(T(
        "Keyflow showcase video: the GPU stage playing a score",
        "Video giới thiệu Keyflow: sân khấu GPU đang chơi một bản nhạc"))
    video_html = (
        '<figure class="shot" style="margin:0"><div class="frame">'
        '<video controls muted loop playsinline preload="metadata" width="1080" height="608" poster="' + root + 'previews/en/stage-gpu-galaxy.png" data-poster-shot="stage-gpu-galaxy" '
        'data-i18n-attr="aria-label=' + video_label_k + '" aria-label="' + video_label_v.replace('"', "&quot;") + '">'
        '<source src="' + root + 'media/showcase.mp4" type="video/mp4"></video></div>'
        '<figcaption class="frame-cap" data-i18n="' + video_cap_k + '">' + video_cap_v + "</figcaption></figure>"
    )

    def shot_items(names, captions, titles=None):
        """Slides for ``slider``: ``titles`` are the short picker labels (tabs and steps)."""
        titles = titles or [None] * len(names)
        return [dict(shot=n, cap=c, **({"title": t} if t else {})) for n, c, t in zip(names, captions, titles)]

    body = [
        pagehero(
            crumbs=[],
            crumb=T("Gallery", "Hình ảnh"),
            eyebrow=T("Gallery", "Hình ảnh"),
            title=T("Real Keyflow captures, with no stock artwork",
                    "Ảnh chụp thực tế từ Keyflow, không ảnh minh hoạ có sẵn"),
            lead=T("The app screenshots here are rendered by Keyflow in CI with <code>--snapshot</code> in English "
                   "and Tiếng Việt. Use the header switch to change those screenshots; the side-by-side preset "
                   "comparison is a fixed English-language image.",
                   "Ảnh chụp ứng dụng tại đây được Keyflow render trong CI bằng <code>--snapshot</code> ở cả English "
                   "và Tiếng Việt. Dùng công tắc ở đầu trang để đổi các ảnh đó; ảnh so sánh preset đặt cạnh nhau là "
                   "ảnh tĩnh có nhãn tiếng Anh."),
            chips=[
                T("14 screenshots × 2 languages", "14 ảnh chụp × 2 ngôn ngữ"),
                T("1 showcase video", "1 video giới thiệu"),
                T("14 presets, both engines", "14 preset, cả hai engine"),
                T("Click any picture to enlarge", "Bấm vào ảnh bất kỳ để phóng to"),
            ],
            actions=[DOWNLOAD,
                     {"label": T("How the pictures are made", "Những bức ảnh được tạo ra thế nào"),
                      "href": "#how", "kind": "btn-ghost", "icon": "info"}],
            media=framed(doc, "stage-gpu-galaxy",
                         T("Galaxy Voyage on the GPU stage", "Galaxy Voyage trên sân khấu GPU"),
                         T("Galaxy Voyage: rainbow trails over a cosmic ambient layer, drawn by the Direct3D 11 "
                           "engine.",
                           "Galaxy Voyage: vệt cầu vồng trên lớp nền vũ trụ, do engine Direct3D 11 vẽ."),
                         badge=T("GPU stage", "Sân khấu GPU"), lazy=False),
        ),

        slider(
            id="stage",
            variant="spotlight", autoplay=True, interval=5500,
            label=T("The GPU stage: five looks", "Sân khấu GPU: năm diện mạo"),
            eyebrow=T("The stage", "Sân khấu"),
            title=T("What the GPU engine draws", "Những gì engine GPU vẽ ra"),
            sub=T("Five looks of the same engine, changing by themselves. Use the arrow buttons, the bars below or the "
                  "left and right arrow keys to choose one, or press pause to stay on a picture.",
                  "Năm diện mạo của cùng một engine, tự chuyển cảnh. Dùng nút mũi tên, các thanh bên dưới hoặc phím "
                  "mũi tên trái/phải để chọn, hoặc bấm tạm dừng để dừng lại ở một ảnh."),
            slides=shot_items(STAGE_SHOTS, [
                T("Live play: only the notes you play, the glowing hit line, sparks and the transport bar",
                  "Chơi trực tiếp: chỉ những nốt bạn chơi, đường chạm phát sáng, tia lửa và thanh transport"),
                T("Neon Violet, the default look, with a chord being held",
                  "Neon Violet, diện mạo mặc định, với một hợp âm đang giữ"),
                T("Galaxy Voyage: rainbow trails over a cosmic layer",
                  "Galaxy Voyage: vệt cầu vồng trên nền vũ trụ"),
                T("Electric Storm: speed lines and arcs between the keys you hold",
                  "Electric Storm: vệt tốc độ và tia điện giữa các phím đang giữ"),
                T("Your own picture behind the keys, centre-cropped and dimmed 30/100",
                  "Ảnh của bạn sau bàn phím, cắt giữa và làm tối 30/100"),
            ]),
        ),

        slider(
            id="interface",
            variant="tabs", autoplay=False, interval=8000,
            label=T("The Keyflow interface: four pages", "Giao diện Keyflow: bốn trang"),
            eyebrow=T("The interface", "Giao diện"),
            title=T("Three concert interfaces and the design dock",
                    "Ba giao diện hoà nhạc và bàn thiết kế"),
            sub=T("These screenshots are full of small print, so they wait for you: pick a page from the list or use "
                  "the arrows. Press play if you would rather watch them go by.",
                  "Những ảnh chụp này có nhiều chữ nhỏ nên chúng đợi bạn: chọn một trang trong danh sách hoặc dùng "
                  "mũi tên. Bấm phát nếu bạn muốn xem chúng tự chạy."),
            slides=shot_items(UI_SHOTS, [
                T("The Concert Grand start menu, with the interface-language chips",
                  "Menu khởi động Concert Grand, kèm chip chọn ngôn ngữ giao diện"),
                T("The Style page: presets, quick layer switches and the share code",
                  "Trang Style: preset, công tắc bật nhanh từng lớp và mã chia sẻ"),
                T("The Theme page: three interfaces, the theme studio and the quick looks",
                  "Trang Theme: ba giao diện, xưởng theme và các look nhanh"),
                T("The General page in Vietnamese: language, graphics engine and settings profile",
                  "Trang General tiếng Việt: ngôn ngữ, engine đồ hoạ và hồ sơ cài đặt"),
            ], [
                T("Start menu", "Menu khởi động"),
                T("Style page", "Trang Style"),
                T("Theme page", "Trang Theme"),
                T("General page", "Trang General"),
            ]),
        ),

        slider(
            id="session",
            variant="steps", autoplay=True, interval=7000, stop_on_interact=True,
            label=T("A session in five steps", "Một phiên làm việc trong năm bước"),
            eyebrow=T("The session", "Phiên làm việc"),
            title=T("Choosing a score, practising, recording", "Chọn bài, luyện tập, ghi hình"),
            sub=T("Five steps in the order you meet them. They advance slowly on their own until you take over "
                  "with the arrows or by choosing a step.",
                  "Năm bước theo đúng thứ tự bạn gặp. Chúng tự chuyển chậm cho tới khi bạn tự điều khiển "
                  "bằng mũi tên hoặc chọn một bước."),
            slides=shot_items(SESSION_SHOTS, [
                T("The Play dialog: score chooser, per-hand presets, recent songs and the library",
                  "Hộp thoại Play: bộ chọn bài, preset từng tay, bài gần đây và thư viện"),
                T("Practice: modes, tempo and the A-B loop",
                  "Luyện tập: chế độ tập, tempo và vòng lặp A-B"),
                T("History: every run of the open song, the chart and the ghost",
                  "Lịch sử: từng lượt chơi của bài đang mở, biểu đồ và bóng luyện tập"),
                T("Recording: format, resolution, frame rate, audio and transparency",
                  "Ghi hình: định dạng, độ phân giải, tốc độ khung hình, tiếng và nền trong suốt"),
                T("The F1 card: every shortcut, in three groups",
                  "Thẻ F1: mọi phím tắt, chia ba nhóm"),
            ], [
                T("Choose a score", "Chọn bản nhạc"),
                T("Practise", "Luyện tập"),
                T("Review history", "Xem lịch sử"),
                T("Record", "Ghi hình"),
                T("Shortcuts", "Phím tắt"),
            ]),
        ),

        split(
            id="presets",
            eyebrow=T("All presets", "Tất cả preset"),
            title=T("Fourteen looks, two engines, one picture", "Mười bốn diện mạo, hai engine, một bức ảnh"),
            body=[T("The CI pipeline renders every built-in preset twice — once with the software renderer and once "
                    "with the GPU engine — and lays the results out in a single tall picture. It is the quickest way "
                    "to compare looks, and the way the project proves the GPU stage kept each theme's intent.",
                    "Quy trình CI render mọi preset dựng sẵn hai lần — một bằng bộ dựng hình phần mềm và một bằng "
                    "engine GPU — rồi xếp kết quả vào một bức ảnh dọc duy nhất. Đó là cách nhanh nhất để so sánh các "
                    "look, và là cách dự án chứng minh sân khấu GPU giữ đúng ý đồ của từng chủ đề.")],
            ticks=[
                E("Neon Violet, Inferno, Aurora Rainbow, Ice Crystal, Two Hands, Classic Roll and Green Screen"),
                T("Sakura Nocturne, Concert Gold, Moonlight Sonata, Galaxy Voyage, Electric Storm, Ocean Depths and "
                  "Retro Arcade",
                  "Sakura Nocturne, Concert Gold, Moonlight Sonata, Galaxy Voyage, Electric Storm, Ocean Depths "
                  "và Retro Arcade"),
                T("Plus three community presets embedded in the build, labelled COMMUNITY in the list.",
                  "Cộng thêm ba preset cộng đồng nhúng trong bản dựng, dán nhãn COMMUNITY trong danh sách."),
            ],
            actions=[{"label": T("Open the full preset sheet", "Mở bảng preset đầy đủ"),
                      "href": "previews/presets.jpg", "kind": "btn-ghost", "icon": "grid", "external": True},
                     {"label": T("Presets & themes", "Preset & theme"),
                      "href": "features/design.html", "kind": "btn-quiet", "icon": "palette"}],
            media=framed(doc, "stage-gpu-storm",
                         T("Electric Storm on the GPU stage", "Electric Storm trên sân khấu GPU"),
                         T("Electric Storm: one of the fourteen looks, here on the GPU engine.",
                           "Electric Storm: một trong mười bốn look, ở đây chạy trên engine GPU."),
                         badge=T("GPU stage", "Sân khấu GPU")),
        ),

        raw('<section class="section" id="presets-sheet"><div class="container">'
            + '<div class="section-head"><p class="eyebrow" data-i18n="' + presets_k + '">' + presets_v + "</p>"
            + '<h2 data-i18n="' + doc.key(T("The whole sheet", "Cả bảng preset"))[0] + '">'
            + doc.key(T("The whole sheet", "Cả bảng preset"))[1] + "</h2></div>"
            + presets_html + "</div></section>"),

        raw('<section class="section" id="video"><div class="container">'
            + '<div class="section-head"><p class="eyebrow" data-i18n="'
            + doc.key(T("In motion", "Chuyển động"))[0] + '">' + doc.key(T("In motion", "Chuyển động"))[1] + "</p>"
            + '<h2 data-i18n="' + doc.key(T("One take, no editing", "Một lượt quay, không dựng"))[0] + '">'
            + doc.key(T("One take, no editing", "Một lượt quay, không dựng"))[1] + "</h2></div>"
            + video_html + "</div></section>"),

        callout(
            id="how",
            style="tip",
            icon="camera",
            title=T("How these pictures are made", "Những bức ảnh này được tạo ra thế nào"),
            body=[
                T("Keyflow can render its own interface: <code>--snapshot</code> draws a window off-screen and writes "
                  "it out, <code>--show-settings --settings-tab=…</code> opens straight on a dock page, "
                  "<code>--play-chord</code> holds a chord so the stage is not empty, and <code>--lang=vi</code> "
                  "renders the whole interface in Vietnamese for that one run without touching your settings.",
                  "Keyflow tự render được giao diện của mình: <code>--snapshot</code> vẽ một cửa sổ off-screen rồi "
                  "ghi ra tệp, <code>--show-settings --settings-tab=…</code> mở thẳng vào một trang của dock, "
                  "<code>--play-chord</code> giữ một hợp âm để sân khấu không trống trải, và <code>--lang=vi</code> "
                  "vẽ toàn bộ giao diện bằng tiếng Việt cho riêng lượt chạy đó mà không đụng tới cài đặt của bạn."),
                T("CI renders on WARP — Windows' own software rasterizer — so the pictures are reproducible on a "
                  "runner with no graphics card, and they are re-rendered whenever the interface changes.",
                  "CI render bằng WARP — bộ dựng hình phần mềm của chính Windows — nên ảnh có thể tái tạo trên một "
                  "máy chạy CI không có card đồ hoạ, và chúng được render lại mỗi khi giao diện thay đổi."),
            ],
        ),

        cta(
            title=T("Your stage will look like this", "Sân khấu của bạn sẽ trông như thế này"),
            sub=T("Free and MIT licensed. Every app screenshot in this gallery shows the real interface — not stock artwork.",
                  "Miễn phí và theo giấy phép MIT. Mọi ảnh chụp ứng dụng trong thư viện đều là giao diện thật, không phải ảnh minh hoạ có sẵn."),
            actions=[DOWNLOAD,
                     {"label": T("Read the guide", "Đọc hướng dẫn"), "href": "guide.html",
                      "kind": "btn-ghost", "icon": "book"}],
        ),
    ]
    return {
        "title": T("Gallery: real Keyflow screenshots & video",
                   "Thư viện ảnh: ảnh chụp & video thực tế từ Keyflow"),
        "description": T(
            "Explore app-rendered screenshots in English and Tiếng Việt, the Keyflow showcase video, and a side-by-side "
            "comparison of all fourteen presets across its software and GPU renderers.",
            "Khám phá ảnh chụp ứng dụng bằng English và Tiếng Việt, video giới thiệu Keyflow, cùng ảnh so sánh cả "
            "mười bốn preset giữa bộ dựng hình phần mềm và GPU."),
        "og_image": "previews/en/stage-gpu-storm.png",
        "body": body,
    }


# ===========================================================================
# Guide
# ===========================================================================
def build_guide(doc) -> dict:
    body = [
        pagehero(
            crumbs=[],
            crumb=T("Guide", "Hướng dẫn"),
            eyebrow=T("Guide & reference", "Hướng dẫn & tra cứu"),
            title=T("From installing to performing, without opening the documentation",
                    "Từ lúc cài đặt tới lúc biểu diễn, không cần mở tài liệu"),
            lead=T("First-time setup, the shortcuts card, the interface map, where your settings live, the command "
                   "line, the built-in verification suite, the honest limitations and the licence — all on one page.",
                   "Thiết lập lần đầu, thẻ phím tắt, bản đồ giao diện, nơi lưu cài đặt, dòng lệnh, bộ kiểm chứng "
                   "tích hợp, những giới hạn nói thẳng và giấy phép — tất cả trong một trang."),
            chips=[
                T("7 setup steps", "7 bước thiết lập"),
                T("16 shortcuts", "16 phím tắt"),
                T("13 dock pages", "13 trang dock"),
                T("10 command-line flags", "10 cờ dòng lệnh"),
            ],
            actions=[DOWNLOAD,
                     {"label": T("Full documentation on GitHub", "Tài liệu đầy đủ trên GitHub"),
                      "href": README_EN, "kind": "btn-ghost", "icon": "book", "external": True}],
            media=framed(doc, "shortcuts",
                         T("The in-app shortcuts card", "Thẻ phím tắt trong ứng dụng"),
                         T("The F1 card inside the app lists exactly the shortcuts on this page, in your language.",
                           "Thẻ F1 trong ứng dụng liệt kê đúng những phím tắt ở trang này, bằng ngôn ngữ của bạn."),
                         badge=T("Press F1 in the app", "Bấm F1 trong ứng dụng"), lazy=False),
        ),

        steps(
            id="setup",
            numbered=True,
            eyebrow=T("First-time setup", "Thiết lập lần đầu"),
            title=T("Seven things worth knowing before you play", "Bảy điều nên biết trước khi chơi"),
            items=[
                {"t": T("Audio output", "Đầu ra âm thanh"),
                 "d": T("Keyflow plays through the default Windows output device (waveOut). Change speakers or "
                        "headphones in Windows Settings → System → Sound before opening the app.",
                        "Keyflow phát qua thiết bị đầu ra mặc định của Windows (waveOut). Đổi loa hoặc tai nghe "
                        "trong Windows Settings → System → Sound trước khi mở ứng dụng.")},
                {"t": T("The SoundFont loads itself", "SoundFont tự nạp"),
                 "d": T("The bundled Yamaha grand loads at startup — a few seconds, and the label on the Audio page "
                        "says when it is ready. For another piano: SETTINGS → Audio → LOAD SOUNDFONT, pick a .sf2, "
                        "then a bank/program preset. HALL REVERB toggles the room.",
                        "Grand Yamaha đi kèm được nạp lúc khởi động — vài giây, và nhãn trên trang Audio báo khi "
                        "xong. Muốn dùng piano khác: SETTINGS → Audio → LOAD SOUNDFONT, chọn tệp .sf2, rồi chọn "
                        "preset bank/program. Nút HALL REVERB bật/tắt tiếng vang phòng.")},
                {"t": T("Your MIDI keyboard", "Đàn MIDI của bạn"),
                 "d": T("Plug it in before launching and Keyflow connects the first input by itself. Plugged in "
                        "later? SETTINGS → MIDI → Refresh devices. The badge above the keyboard reads MIDI IN · C4 "
                        "when a note arrives.",
                        "Cắm đàn trước khi mở ứng dụng thì Keyflow tự kết nối ngõ vào đầu tiên. Cắm sau? Mở "
                        "SETTINGS → MIDI → Refresh devices. Nhãn phía trên bàn phím hiện MIDI IN · C4 khi có nốt vào.")},
                {"t": T("Graphics need nothing", "Đồ hoạ không cần bật gì"),
                 "d": T("The stage runs on the GPU from the first launch. Frame rate, VSync, the second-screen stage "
                        "window and the engine status line live in SETTINGS → General → GRAPHICS ENGINE — settings of "
                        "the machine, so presets never change them.",
                        "Sân khấu chạy bằng GPU ngay từ lần mở đầu. Tốc độ khung hình, VSync, cửa sổ sân khấu cho "
                        "màn hình thứ hai và dòng trạng thái engine nằm ở SETTINGS → General → GRAPHICS ENGINE — "
                        "đây là thiết lập của máy nên áp preset không đổi chúng.")},
                {"t": T("Pick a look", "Chọn diện mạo"),
                 "d": T("SETTINGS → Style for the preset (Neon Violet by default), SETTINGS → Theme for the concert "
                        "interface (Concert Grand by default), then fine-tune on Notes, Particles, Keyboard, "
                        "Background and Camera & FX. Every change applies live and saves itself.",
                        "SETTINGS → Style để chọn preset (mặc định Neon Violet), SETTINGS → Theme để chọn giao diện "
                        "hoà nhạc (mặc định Concert Grand), rồi tinh chỉnh ở Notes, Particles, Keyboard, Background "
                        "và Camera & FX. Mọi thay đổi áp dụng ngay và tự lưu.")},
                {"t": T("Where settings live", "Cài đặt nằm ở đâu"),
                 "d": T("%LOCALAPPDATA%\\Keyflow holds visual-settings.json, library.json, history\\practice.jsonl, "
                        "presets\\*.json and themes\\*.json. Move everything with --settings-dir=&lt;folder&gt;, or press "
                        "RESET TO DEFAULT in the dock.",
                        "%LOCALAPPDATA%\\Keyflow chứa visual-settings.json, library.json, history\\practice.jsonl, "
                        "presets\\*.json và themes\\*.json. Dời tất cả bằng --settings-dir=&lt;thư mục&gt;, hoặc bấm "
                        "RESET TO DEFAULT trong dock.")},
                {"t": T("Recording", "Ghi hình"),
                 "d": T("On the Recording page choose Format — AVI, a 32-bit PNG sequence with alpha, or MP4 with the "
                        "sound inside — plus Resolution and Frame rate. Then press REC in the corner of the stage, "
                        "choose where it goes, and press again to stop.",
                        "Ở trang Recording chọn Format — AVI, chuỗi PNG 32-bit có alpha, hoặc MP4 kèm tiếng — cùng "
                        "Resolution và Frame rate. Sau đó bấm REC ở góc sân khấu, chọn nơi lưu và bấm lại để dừng.")},
            ],
        ),

        steps(
            id="start",
            numbered=True,
            eyebrow=T("Getting started", "Bắt đầu sử dụng"),
            title=T("Five moves from the menu to a playing score", "Năm thao tác từ menu tới một bản nhạc đang chạy"),
            items=[
                {"t": T("The concert menu", "Menu hoà nhạc"),
                 "d": T("The app opens on a menu: Perform & Play, Quick Adjustments, Stage Design Studio, Audio & "
                        "MIDI Hardware Setup, Keyboard & Shortcuts, About, Exit. HOME on the header comes back to it "
                        "at any time.",
                        "Ứng dụng khởi động ở menu hoà nhạc: Perform & Play, Quick Adjustments, Stage Design Studio, "
                        "Audio & MIDI Hardware Setup, Keyboard & Shortcuts, About, Exit. Nút HOME trên header quay "
                        "lại menu bất cứ lúc nào.")},
                {"t": T("Live Play first", "Chơi trực tiếp trước"),
                 "d": T("Press a key on the piano, the computer keyboard or a MIDI instrument and only the notes you "
                        "play appear. The Yamaha grand is already loaded, so everything sounds immediately; HALL "
                        "toggles the concert reverb.",
                        "Nhấn một phím trên piano, bàn phím máy tính hoặc đàn MIDI và chỉ những nốt bạn chơi hiện "
                        "ra. SoundFont grand Yamaha đã nạp sẵn nên mọi thứ phát tiếng ngay; nút HALL bật/tắt reverb "
                        "phòng hoà nhạc.")},
                {"t": T("Open the session dialog", "Mở hộp thoại phiên"),
                 "d": T("Play on the header (or Perform & Play) opens it: choose a MIDI file or a MusicXML score, or "
                        "Live Play. The button reads Choose a MIDI file, then Start playback, then Return to "
                        "playback — it never restarts your song by accident.",
                        "Play trên header (hoặc Perform & Play) sẽ mở hộp thoại: chọn tệp MIDI, bản MusicXML, hoặc "
                        "Live Play. Nút ghi Choose a MIDI file, rồi Start playback, rồi Return to playback — không "
                        "bao giờ khởi động lại bài vì bấm nhầm.")},
                {"t": T("Play along", "Chơi theo"),
                 "d": T("Notes travel down and touch the glowing line just above the keys. Play along and get "
                        "hit/miss feedback, accuracy and streak under the stage.",
                        "Nốt đi xuống và chạm đường sáng ngay trên phím đàn. Chơi theo và nhận phản hồi đúng/sai, "
                        "độ chính xác cùng chuỗi đúng liên tiếp dưới sân khấu.")},
                {"t": T("Esc goes back in order", "Esc quay lại theo thứ tự"),
                 "d": T("Esc steps back through the surfaces you opened: Quick Adjust → Play → settings → menu → "
                        "stage; on the stage it opens the dock, clearing the settings search and closing the F1 card "
                        "first.",
                        "Esc quay lại theo đúng thứ tự bề mặt đang mở: Quick Adjust → Play → cài đặt → menu → sân "
                        "khấu; ở màn hình sân khấu nó mở dock, xoá ô tìm kiếm và đóng thẻ F1 trước.")},
            ],
        ),

        table(
            id="shortcuts",
            eyebrow=T("Keyboard & shortcuts", "Bàn phím & phím tắt"),
            title=T("The same table the F1 card shows", "Đúng bảng mà thẻ F1 hiển thị"),
            sub=T("Three groups, exactly as the in-app card lists them — so you never need this page open while "
                  "playing.",
                  "Ba nhóm, đúng như thẻ trong ứng dụng liệt kê — nên bạn không cần mở trang này lúc đang chơi."),
            head=[T("Group", "Nhóm"), T("Key or action", "Phím / thao tác"), T("What it does", "Tác dụng")],
            rows=[
                [{"html": '<b>' + doc.key(T("Play the stage", "Chơi nhạc"))[1] + "</b>"},
                 {"html": kbd("A", "W", "S", "E", "D", "F", "T", "G", "Y", "H", "U", "J", "K")},
                 T("One octave from middle C (C4); hold a key to sustain the note, release it to send Note Off.",
                   "Một quãng tám từ nốt giữa (C4); nhấn giữ để duy trì nốt, thả ra để gửi Note Off.")],
                [{"html": '<b>' + doc.key(T("Play the stage", "Chơi nhạc"))[1] + "</b>"}, {"html": kbd("Space")},
                 T("Start or pause the loaded MIDI score.", "Phát hoặc tạm dừng bài MIDI đang mở.")],
                [{"html": '<b>' + doc.key(T("Play the stage", "Chơi nhạc"))[1] + "</b>"},
                 T("Click the keys", "Click lên phím đàn"),
                 T("Play the on-screen piano with the full colour, spark and flame response.",
                   "Chơi piano ảo với đầy đủ phản hồi màu, tia lửa và lửa.")],
                [{"html": '<b>' + doc.key(T("Play the stage", "Chơi nhạc"))[1] + "</b>"},
                 T("MIDI keyboard", "Đàn MIDI"),
                 T("Velocity, Note On/Off and the three pedals (CC 64/66/67) enter the same feedback pipeline.",
                   "Velocity, Note On/Off và ba pedal (CC 64/66/67) đi vào cùng luồng phản hồi.")],
                [{"html": '<b>' + doc.key(T("Move around", "Điều hướng"))[1] + "</b>"}, {"html": kbd("F11")},
                 T("Toggle full screen.", "Bật/tắt toàn màn hình.")],
                [{"html": '<b>' + doc.key(T("Move around", "Điều hướng"))[1] + "</b>"}, {"html": kbd("F1")},
                 T("Open or close the shortcuts card.", "Mở hoặc đóng thẻ phím tắt.")],
                [{"html": '<b>' + doc.key(T("Move around", "Điều hướng"))[1] + "</b>"}, {"html": kbd("Tab")},
                 T("Open the Play dialog from the stage; in menus and dialogs Tab still moves focus normally.",
                   "Mở hộp thoại Play từ sân khấu; trong menu và hộp thoại, Tab vẫn chuyển tiêu điểm như bình thường.")],
                [{"html": '<b>' + doc.key(T("Move around", "Điều hướng"))[1] + "</b>"}, {"html": kbd("Esc")},
                 T("Go back through the open surface (Quick Adjust → Play → settings → menu → stage); on the stage "
                   "it opens the dock.",
                   "Quay lại theo thứ tự bề mặt đang mở (Quick Adjust → Play → cài đặt → menu → sân khấu); ở sân "
                   "khấu thì mở dock.")],
                [{"html": '<b>' + doc.key(T("Move around", "Điều hướng"))[1] + "</b>"},
                 {"html": kbd("Ctrl+Z") + " / " + kbd("Ctrl+Shift+Z")},
                 T("Undo and redo in the design dock: 32 states, one slider drag counts as one step, and it never "
                   "steals the undo of the box you are typing in.",
                   "Hoàn tác và làm lại trong bàn thiết kế: 32 trạng thái, một lần kéo slider tính là một bước, và "
                   "không giành quyền hoàn tác của ô bạn đang gõ.")],
                [{"html": '<b>' + doc.key(T("Move around", "Điều hướng"))[1] + "</b>"},
                 T("Leave the pointer still for ~2.8 s", "Để chuột yên khoảng 2,8 giây"),
                 T("The whole interface hides — header, transport, Menu, REC and the dock — leaving only the piano, "
                   "the background and the notes. It never hides while you drag a slider, open a drop-down, use the "
                   "colour picker, read the shortcuts card or type in settings.",
                   "Toàn bộ giao diện tự ẩn — thanh trên/dưới, Menu, REC và cả dock — chỉ còn đàn, nền và nốt. "
                   "Giao diện không tự ẩn khi đang kéo slider, mở danh sách chọn, mở bảng chọn màu, đang mở thẻ phím "
                   "tắt, hoặc đang gõ trong bảng cài đặt.")],
                [{"html": '<b>' + doc.key(T("Session & capture", "Phiên & ghi hình"))[1] + "</b>"},
                 {"html": kbd("A") + " " + kbd("B") + " " + kbd("×")},
                 T("Set or clear the A-B loop at the playhead.", "Đặt hoặc xoá vòng lặp A–B tại playhead.")],
                [{"html": '<b>' + doc.key(T("Session & capture", "Phiên & ghi hình"))[1] + "</b>"},
                 T("Drag the timeline", "Kéo thanh thời gian"),
                 T("Seek in the score; notes you skip are not counted as misses.",
                   "Tua bài; nốt bị bỏ qua không tính là miss.")],
                [{"html": '<b>' + doc.key(T("Session & capture", "Phiên & ghi hình"))[1] + "</b>"},
                 T("Practice page", "Trang Practice"),
                 T("Follow along, Wait for my note, Right hand only, Left hand only; tempo 50–150%.",
                   "Chơi theo, chờ nốt của tôi, chỉ tay phải, chỉ tay trái; tempo 50–150%.")],
                [{"html": '<b>' + doc.key(T("Session & capture", "Phiên & ghi hình"))[1] + "</b>"},
                 {"html": "<b>REC</b>"},
                 T("Record the stage to AVI, to a folder of 32-bit PNG frames with alpha, or to an MP4 with the audio "
                   "already inside it.",
                   "Ghi sân khấu ra AVI, ra thư mục khung PNG 32-bit có alpha, hoặc ra MP4 đã có sẵn âm thanh "
                   "trong tệp.")],
            ],
        ),

        table(
            id="interface",
            eyebrow=T("Interface map", "Bản đồ giao diện"),
            title=T("Four areas around the stage", "Bốn khu vực quanh sân khấu"),
            head=[T("Area", "Khu vực"), T("What is there", "Có gì ở đó")],
            rows=[
                [T("Header", "Thanh trên"),
                 T("Logo and brand, the open song, the LOOK chip with the current preset and a Change button, HOME, "
                   "Play (score chooser, Live Play and quick settings), SETTINGS, and minimize / full screen / exit.",
                   "Logo và tên ứng dụng, bài đang mở, chip LOOK với preset hiện tại cùng nút Change, HOME, Play "
                   "(chọn bài, Live Play và cài đặt nhanh), SETTINGS, thu nhỏ / toàn màn hình / thoát.")],
                [T("Stage", "Sân khấu"),
                 T("Notes and effects, the keyboard, the device badge, the REC button and the MENU button.",
                   "Nốt và hiệu ứng, bàn phím, nhãn thiết bị, nút REC và nút MENU.")],
                [T("Footer", "Thanh dưới"),
                 T("Play/Pause, back to the start, time and the note being played, the three pedals, ACCURACY / "
                   "SCORE / STREAK, and the seek bar with progress.",
                   "Play/Pause, quay lại đầu, thời gian và nốt đang chơi, ba pedal, ACCURACY / SCORE / STREAK, "
                   "cùng thanh tua và tiến trình.")],
                [T("Settings dock", "Bàn cài đặt"),
                 T("A navigation column of four groups, a search box that covers every page and jumps to the first "
                   "result, a slider plus a numeric box plus a reset per parameter, rows that hide and show "
                   "themselves, SAVE and RESET PAGE, and autosave after 0.65 s.",
                   "Cột điều hướng bốn nhóm, ô tìm kiếm bao trùm mọi trang và tự nhảy tới kết quả đầu tiên, mỗi "
                   "thông số có thanh trượt kèm ô nhập số và nút reset, các hàng tự ẩn/hiện, SAVE và RESET PAGE, "
                   "tự lưu sau 0,65 giây.")],
            ],
            note=T("The thirteen dock pages, grouped into Stage design, Sound & input, Session and App, are listed on "
                   "the design page.",
                   "Mười ba trang của dock, chia thành Thiết kế sân khấu, Âm thanh & đầu vào, Phiên làm việc và Ứng "
                   "dụng, được liệt kê ở trang thiết kế."),
            actions=[{"label": T("The thirteen dock pages", "Mười ba trang dock"),
                      "href": "features/design.html#pages", "kind": "btn-ghost", "icon": "sliders"}],
        ),

        split(
            id="languages",
            flip=True,
            eyebrow=T("Languages", "Ngôn ngữ"),
            title=T("Two languages, three ways to switch, and three rules",
                    "Hai ngôn ngữ, ba cách đổi, và ba nguyên tắc"),
            ticks=[
                T("General page (dock → APP): choose English, Tiếng Việt or Follow Windows; the line underneath says "
                  "which language is running and where the choice came from.",
                  "Trang General (dock → APP): chọn English, Tiếng Việt hoặc Theo Windows; dòng mô tả bên dưới ghi "
                  "rõ ngôn ngữ nào đang chạy và nó được chọn từ đâu."),
                T("Start menu: the INTERFACE LANGUAGE chips change it on the very first launch, before you have found "
                  "any settings page.",
                  "Menu khởi động: thẻ INTERFACE LANGUAGE đổi ngôn ngữ ngay lần mở đầu, trước khi bạn kịp tìm trang "
                  "cài đặt nào."),
                T("Command line: <code>--lang=vi</code> (or <code>en</code>) runs once in that language and does not "
                  "write to visual-settings.json — which is how CI renders the Vietnamese pictures.",
                  "Dòng lệnh: <code>--lang=vi</code> (hoặc <code>en</code>) chạy một lần bằng ngôn ngữ chỉ định và "
                  "không ghi vào visual-settings.json — đây là cách CI render bộ ảnh tiếng Việt."),
                T("Rule one — ids never change, only captions do: values in visual-settings.json, preset names, theme "
                  "ids, Windows device names and file names stay English, so switching language cannot break a saved "
                  "preset and a preset travels to an English machine.",
                  "Nguyên tắc một — id không đổi, chỉ caption đổi: giá trị trong visual-settings.json, tên preset, "
                  "id theme, tên thiết bị Windows và tên tệp luôn là tiếng Anh, nên bật tiếng Việt không làm hỏng "
                  "preset hay tệp đã lưu, và một preset đem sang máy tiếng Anh vẫn đọc được."),
                T("Rule two — a missing translation prints English, never an empty box; unknown keys such as device "
                  "names and user file names reach the screen verbatim.",
                  "Nguyên tắc hai — thiếu bản dịch thì in tiếng Anh, không in ô trống; khoá lạ không có trong "
                  "inventory (tên thiết bị, tên tệp người dùng đặt) đi thẳng tới màn hình nguyên văn."),
                T("Rule three — adding a language means adding one table file: copy the English strings, translate "
                  "the values, add a line to the language list; the renderer, the XAML and the settings file need no "
                  "change, and a static check proves the new table covers every key.",
                  "Nguyên tắc ba — thêm ngôn ngữ là thêm một tệp bảng: sao chép bảng tiếng Anh, dịch phần giá trị, "
                  "thêm một dòng vào danh sách ngôn ngữ; renderer, XAML và tệp cài đặt không phải sửa gì, và một "
                  "kiểm tra tĩnh chứng minh bảng mới dịch đủ mọi khoá."),
            ],
            actions=[{"label": T("This site in Tiếng Việt", "Trang này bằng Tiếng Việt"),
                      "href": "index.html?lang=vi", "kind": "btn-ghost", "icon": "globe"}],
            media=framed(doc, "language-dock",
                         T("The General page running in Vietnamese", "Trang General khi chạy bằng tiếng Việt"),
                         T("Every label, hint and button in Vietnamese; the preset name Neon Violet stays as it is, "
                           "because that is a saved id.",
                           "Toàn bộ nhãn, chú thích và nút bằng tiếng Việt; tên preset Neon Violet vẫn giữ nguyên vì "
                           "đó là id đã lưu."),
                         badge=T("Tiếng Việt", "Tiếng Việt")),
        ),

        table(
            id="cli",
            eyebrow=T("Command line", "Dòng lệnh"),
            title=T("Flags worth knowing", "Những cờ đáng biết"),
            sub=T("Run them against PianoPath.exe — the single executable inside every package.",
                  "Chạy chúng với PianoPath.exe — tệp thực thi duy nhất trong mỗi gói."),
            head=[T("Flag", "Cờ"), T("What it does", "Tác dụng")],
            rows=[
                [{"html": "<code>--lang=vi</code> / <code>en</code>"},
                 T("Run once in that language without saving the choice.",
                   "Chạy một lần bằng ngôn ngữ đó mà không lưu lựa chọn.")],
                [{"html": "<code>--snapshot</code>"},
                 T("Render the interface off-screen and write a screenshot — this is how the app captures used in the galleries "
                   "are made.",
                   "Render giao diện off-screen rồi ghi ảnh ra — đây là cách tạo ảnh chụp ứng dụng trong thư viện.")],
                [{"html": "<code>--show-settings --settings-tab=&lt;page&gt;</code>"},
                 T("Open straight on one dock page.", "Mở thẳng vào một trang của dock.")],
                [{"html": "<code>--play-chord</code>"},
                 T("Start with a chord held, so the stage shows hold effects.",
                   "Khởi động với một hợp âm đang giữ để sân khấu hiện hiệu ứng giữ phím.")],
                [{"html": "<code>--software</code>"},
                 T("Use the software renderer once — the fallback path, and the one that draws transparent PNG takes.",
                   "Dùng bộ dựng hình phần mềm cho một lượt — đường dự phòng, và cũng là đường vẽ bản ghi PNG "
                   "trong suốt.")],
                [{"html": "<code>--background-image=&lt;file.png&gt;</code>"},
                 T("Put a picture behind the keys for this run.", "Đặt một ảnh nền sau bàn phím cho lượt chạy này.")],
                [{"html": "<code>--settings-dir=&lt;folder&gt;</code>"},
                 T("Keep settings, library, history, presets and themes somewhere else.",
                   "Giữ cài đặt, thư viện, lịch sử, preset và theme ở nơi khác.")],
                [{"html": "<code>--verify</code>"},
                 T("Run the built-in verification suite; exit code 0 means pass, 1 means something failed.",
                   "Chạy bộ kiểm chứng tích hợp; mã thoát 0 là đạt, 1 là có lỗi.")],
                [{"html": "<code>--verify-log=&lt;path&gt;</code>"},
                 T("Where to write the PASS/FAIL log (default %TEMP%\\keyflow-verification.log).",
                   "Nơi ghi nhật ký PASS/FAIL (mặc định %TEMP%\\keyflow-verification.log).")],
                [{"html": "<code>--bench</code>"},
                 T("Print a benchmark report, including the version the app reads from its own assembly.",
                   "In báo cáo đo hiệu năng, kèm phiên bản mà ứng dụng tự đọc từ assembly của nó.")],
            ],
        ),

        split(
            id="verify",
            eyebrow=T("Verification suite", "Bộ kiểm chứng"),
            title=T("The app can check itself on your machine", "Ứng dụng tự kiểm tra được ngay trên máy bạn"),
            body=[T("Keyflow ships a verification suite that runs inside the real application — it needs Windows, "
                    "because it starts a real WPF window. It writes each PASS/FAIL line as it goes, so even a crash "
                    "leaves a last line saying what it was doing. Subjects that need hardware you do not have report "
                    "SKIP, which is not a failure.",
                    "Keyflow đi kèm một bộ kiểm chứng chạy ngay trong ứng dụng thật — cần Windows vì nó khởi động "
                    "một cửa sổ WPF thật. Nhật ký ghi từng dòng PASS/FAIL ngay khi mục đó chạy xong, nên kể cả khi "
                    "sập vẫn còn dòng cuối nói nó đang làm gì. Mục cần phần cứng bạn không có sẽ báo SKIP, và đó "
                    "không phải lỗi.")],
            ticks=[
                T("The MIDI parser: multi-track files, tempo maps, the beat grid, meter grouping (4/4, 3/4, 2/2, 3/8 "
                  "and compound 6/8, 9/8, 12/8), format 2 sequences, SMPTE divisions, drum channel, corrupt files.",
                  "Bộ đọc MIDI: tệp đa track, tempo map, lưới phách, nhóm phách theo ô nhịp (4/4, 3/4, 2/2, 3/8 và "
                  "nhịp ghép 6/8, 9/8, 12/8), chuỗi định dạng 2, độ chia SMPTE, kênh trống, tệp hỏng."),
                T("SoundFont decoding and generator semantics, polyphony limits, release loops, the audio signal, "
                  "Note Off and all three pedals.",
                  "Giải mã SoundFont và ngữ nghĩa generator, giới hạn đa âm, vòng qua giai đoạn release, tín hiệu "
                  "âm thanh, Note Off và cả ba pedal."),
                T("Settings save and clamp, presets (save, import, export, delete, corrupt files), preset thumbnails "
                  "and share codes, user themes, the community preset shelf.",
                  "Lưu và kẹp cấu hình, preset (lưu, nhập, xuất, xoá, tệp hỏng), ảnh thu nhỏ của preset và mã chia "
                  "sẻ, theme tự tạo, kệ preset cộng đồng."),
                T("The dock catalogue: thirteen pages in four groups agreeing between the code, the XAML and the "
                  "tests; live language switching on an open window; accessibility names and high contrast.",
                  "Danh mục dock: mười ba trang trong bốn nhóm khớp giữa mã nguồn, XAML và bộ kiểm thử; đổi ngôn ngữ "
                  "trực tiếp trên cửa sổ đang mở; tên trợ năng và high contrast."),
                T("MusicXML import, the sheet layer (key signature, beaming, rests, ties, chords, hand changes), "
                  "hand-split inference, practice tempo, history, ghost and chart, folder library.",
                  "Nhập MusicXML, lớp khuông nhạc (hoá biểu, nối đuôi, dấu nghỉ, dấu luyến, hợp âm, đổi tay), suy "
                  "luận điểm chia tay, tempo luyện tập, lịch sử, bóng và biểu đồ, thư viện theo thư mục."),
                T("Recording: the 44-byte WAV header byte by byte, the PNG sequence with real alpha, the camera "
                  "overlay read back from a take the app just wrote, and one real GPU frame drawn on WARP and read "
                  "back for measuring.",
                  "Ghi hình: header WAV 44 byte đúng từng byte, chuỗi PNG có alpha thật, lớp phủ camera đọc lại từ "
                  "chính bản ghi ứng dụng vừa viết, và một khung GPU thật vẽ trên WARP rồi đọc lại để đo."),
            ],
            media=_verify_card(doc),
        ),

        callout(
            id="privacy",
            style="tip",
            icon="shield",
            title=T("Privacy, plainly", "Nói thẳng về quyền riêng tư"),
            body=[
                T("This website sets no cookies, runs no analytics and loads no third-party script. Its only external "
                  "requests are the fonts from Google Fonts and one call to GitHub's releases API, which is what "
                  "keeps the download buttons pointing at the newest version.",
                  "Trang web này không đặt cookie, không chạy analytics và không nạp script của bên thứ ba. Yêu cầu "
                  "ra ngoài duy nhất là phông chữ từ Google Fonts và một lệnh gọi tới API releases của GitHub — "
                  "chính là thứ giữ cho nút tải về luôn trỏ tới bản mới nhất."),
                T("The application needs no account and no sign-in. Settings, presets, themes, the song library and "
                  "the practice history are plain files under %LOCALAPPDATA%\\Keyflow, and camera frames are read "
                  "locally and drawn locally — nothing is uploaded.",
                  "Ứng dụng không cần tài khoản và không cần đăng nhập. Cài đặt, preset, theme, thư viện bài và lịch "
                  "sử luyện tập là những tệp thường nằm trong %LOCALAPPDATA%\\Keyflow, còn khung hình camera được đọc "
                  "tại máy và vẽ tại máy — không có gì được tải lên."),
            ],
        ),

        table(
            id="limits",
            eyebrow=T("Honest limits", "Giới hạn nói thẳng"),
            title=T("What 1.0.0 does not do", "Những gì bản 1.0.0 chưa làm được"),
            head=[T("Area", "Mảng"), T("The limit", "Giới hạn")],
            rows=[
                [T("Sound", "Âm thanh"),
                 T("Only uncompressed SoundFont 2; .sf3 is not read, and advanced SF2 parts — modulators, instrument "
                   "filters, reverb/chorus — are not fully reproduced, so the sound can differ from a dedicated "
                   "synthesizer depending on the file.",
                   "Chỉ đọc SoundFont 2 không nén; .sf3 chưa hỗ trợ, và một số phần SF2 nâng cao — modulators, bộ "
                   "lọc nhạc cụ, reverb/chorus — chưa được tái tạo đầy đủ, nên âm thanh có thể khác một bộ tổng hợp "
                   "chuyên dụng tùy tệp.")],
                [T("Scores", "Bản nhạc"),
                 T("Advanced MusicXML is still missing: slurs, repeats and several voices joined into one beat. Plain "
                   "MusicXML, including .mxl, reads fine.",
                   "MusicXML nâng cao vẫn còn thiếu: dấu luyến, repeat và nhiều bè ghép phách. MusicXML cơ bản, kể "
                   "cả .mxl, đọc được bình thường.")],
                [T("Recording", "Ghi hình"),
                 T("No direct WebM/VP9 writer — the 32-bit PNG sequence is the alpha path. MP4 depends on Windows' "
                   "own H.264 and AAC encoders.",
                   "Chưa ghi trực tiếp WebM/VP9 — chuỗi PNG 32-bit là đường alpha. MP4 phụ thuộc bộ mã hoá H.264 và "
                   "AAC của chính Windows.")],
                [T("Camera", "Camera"),
                 T("Hand tracking is classical computer vision: with two hands, or a skin-coloured backdrop, only the "
                  "biggest hand is followed, and the finger count needs a large enough hand. No 3D perspective "
                  "camera — the stage is a flat piano roll with slight parallax.",
                  "Theo dõi bàn tay là thị giác máy tính cổ điển: có hai bàn tay hoặc nền trùng màu da thì chỉ bàn "
                  "tay lớn nhất được theo, và số ngón cần bàn tay đủ lớn. Chưa có camera phối cảnh 3D — sân khấu là "
                  "piano roll phẳng với parallax nhẹ.")],
                [T("Stage", "Sân khấu"),
                 T("No particle compute shader, no depth of field, no velocity-buffer motion blur and no camera "
                   "keyframing yet. The staff, hand marker, camera picture, watermark and counters stay WPF vector "
                   "layers over the GPU frame.",
                   "Chưa có particle compute shader, độ sâu trường ảnh, motion blur theo velocity buffer hay "
                   "keyframe camera. Khuông nhạc, điểm đánh dấu tay, hình camera, watermark và bộ đếm vẫn là lớp "
                   "vector WPF phủ lên khung GPU.")],
                [T("Platform", "Nền tảng"),
                 T("Windows only: the app is built on WPF and WinMM. A Windows-on-ARM package is published but has "
                   "not been run on real ARM hardware yet.",
                   "Chỉ Windows: ứng dụng dựng trên WPF và WinMM. Gói Windows-on-ARM đã được phát hành nhưng chưa "
                   "chạy thử trên máy ARM thật.")],
            ],
            note=T("The full list, with the reasons, is in the documentation's “Current limitations” section.",
                   "Danh sách đầy đủ kèm lý do nằm ở mục “Current limitations” của tài liệu."),
            actions=[{"label": T("Read the full documentation", "Đọc tài liệu đầy đủ"),
                      "href": README_EN, "kind": "btn-ghost", "icon": "book", "external": True}],
        ),

        specdl(
            id="license",
            eyebrow=T("Licence & credits", "Giấy phép & ghi công"),
            title=T("MIT for the code, CC BY 3.0 for the piano",
                    "MIT cho mã nguồn, CC BY 3.0 cho cây đàn"),
            items=[
                (T("Application licence", "Giấy phép ứng dụng"),
                 T("MIT — LICENSE.txt travels inside every package; keep it when you pass a copy on.",
                   "MIT — LICENSE.txt nằm trong mỗi gói; hãy giữ lại khi bạn chia sẻ bản sao.")),
                (T("Bundled SoundFont", "SoundFont đi kèm"),
                 T("YDP Grand Piano from FreePats, built from a Yamaha Disklavier Pro multisample, under CC BY 3.0; "
                   "the credit is in Assets\\ATTRIBUTION.txt.",
                   "YDP Grand Piano của FreePats, dựng từ multisample Yamaha Disklavier Pro, theo CC BY 3.0; phần "
                   "ghi công nằm trong Assets\\ATTRIBUTION.txt.")),
                (T("Graphics", "Đồ hoạ"),
                 T("The Direct3D 11 engine is built on Vortice.Windows; the HLSL shaders are compiled at startup "
                   "with the d3dcompiler_47.dll that ships with Windows.",
                   "Engine Direct3D 11 dựng trên Vortice.Windows; shader HLSL được biên dịch lúc khởi động bằng "
                   "d3dcompiler_47.dll có sẵn trong Windows.")),
                (T("Authors", "Tác giả"),
                 T("Keyflow is made by Yami, Neyu and Jin. Copyright © 2026 Yami, Neyu, Jin.",
                   "Keyflow do Yami, Neyu và Jin tạo ra. Bản quyền © 2026 Yami, Neyu, Jin.")),
                (T("Reporting a problem", "Báo lỗi"),
                 T("Issues are tracked on GitHub — a screenshot, the settings profile and the verification log make "
                   "a bug report actionable.",
                   "Lỗi được theo dõi trên GitHub — một ảnh chụp, hồ sơ cài đặt và nhật ký kiểm chứng sẽ giúp báo "
                   "cáo lỗi xử lý được ngay.")),
                (T("What changed", "Có gì thay đổi"),
                 T("The changelog records everything a user can see, one entry per release.",
                   "Nhật ký thay đổi ghi lại mọi thứ người dùng nhìn thấy, mỗi bản phát hành một mục.")),
            ],
        ),

        faq(
            id="faq",
            eyebrow=T("Questions", "Câu hỏi"),
            title=T("The ones that come up most", "Những câu hỏi hay gặp nhất"),
            items=[
                {"q": T("Can I move my settings to another computer?",
                        "Tôi chuyển cài đặt sang máy khác được không?"),
                 "a": T("Yes. EXPORT PROFILE… on the General page writes one Keyflow.profile.json carrying the stage "
                        "settings, the language and the interface; drag it onto the window of the other machine to "
                        "apply it. Presets and themes travel as their own JSON files, each preset with a rendered "
                        "thumbnail, and a share code carries a whole look as one line of text.",
                        "Được. EXPORT PROFILE… ở trang General ghi một tệp Keyflow.profile.json chứa cài đặt sân "
                        "khấu, ngôn ngữ và giao diện; kéo tệp đó vào cửa sổ trên máy kia để áp dụng. Preset và theme "
                        "đi theo dạng tệp JSON riêng, mỗi preset kèm ảnh thu nhỏ đã render, còn mã chia sẻ mang cả "
                        "một diện mạo trong một dòng chữ.")},
                {"q": T("Does it work without a graphics card?", "Không có card đồ hoạ thì chạy được không?"),
                 "a": T("Yes. Keyflow tries your graphics card first, then WARP — Windows' software rasterizer running "
                        "the same shaders, just slower — and finally the WPF renderer if Direct3D cannot start at "
                        "all. General → GRAPHICS ENGINE always says which one is drawing and why.",
                        "Được. Keyflow thử card đồ hoạ trước, rồi tới WARP — bộ dựng hình phần mềm của Windows chạy "
                        "cùng shader, chỉ chậm hơn — và cuối cùng là bộ dựng hình WPF nếu Direct3D không khởi động "
                        "được. Trang General → GRAPHICS ENGINE luôn ghi rõ engine nào đang vẽ và vì sao.")},
                {"q": T("Why is my MP4 silent, or missing entirely?", "Vì sao MP4 của tôi không có tiếng, hoặc không ghi được?"),
                 "a": T("MP4 is written by Windows' own encoders. Without an H.264 encoder the format cannot be "
                        "written at all and you get a message with the error code; with H.264 but no AAC encoder the "
                        "take keeps the picture and the dialog says why there is no sound; with no SoundFont loaded "
                        "the recording is picture only. AVI always writes a WAV beside it instead.",
                        "MP4 được ghi bằng bộ mã hoá của chính Windows. Máy không có bộ mã hoá H.264 thì không ghi "
                        "được định dạng này và bạn nhận thông báo kèm mã lỗi; máy có H.264 nhưng thiếu AAC thì bản "
                        "ghi vẫn có hình và hộp thoại nói rõ vì sao thiếu tiếng; máy chưa nạp SoundFont thì chỉ ghi "
                        "hình. Riêng AVI luôn ghi kèm một tệp WAV bên cạnh.")},
                {"q": T("Can I put my own video or webcam on the stage?",
                        "Tôi đưa video hoặc webcam của mình lên sân khấu được không?"),
                 "a": T("Yes — Camera & FX has a webcam overlay that draws a live camera or a looping video file in "
                        "any corner, at 15–60% of the stage width, with mirroring, opacity and a green key. Hand "
                        "tracking works from the same frames and needs no model.",
                        "Được — trang Camera & FX có lớp phủ webcam vẽ một camera trực tiếp hoặc tệp video chạy lặp "
                        "ở bất kỳ góc nào, cỡ 15–60% chiều rộng sân khấu, kèm mirror, opacity và key xanh. Phần theo "
                        "dõi bàn tay dùng chính những khung hình đó và không cần mô hình nào.")},
                {"q": T("Is there a macOS or Linux version?", "Có bản macOS hoặc Linux không?"),
                 "a": T("Not in 1.0.0. Keyflow is built on WPF and WinMM and records through Windows' Media "
                        "Foundation, so this version is Windows-only. Windows on ARM has a published package that has "
                        "not been tested on real ARM hardware yet.",
                        "Bản 1.0.0 thì chưa. Keyflow dựng trên WPF và WinMM, ghi hình qua Media Foundation của "
                        "Windows, nên phiên bản này chỉ dành cho Windows. Windows on ARM có gói đã phát hành nhưng "
                        "chưa được chạy thử trên máy ARM thật.")},
                {"q": T("How do I reset everything?", "Làm sao để đưa mọi thứ về mặc định?"),
                 "a": T("RESET TO DEFAULT in the dock, or delete visual-settings.json in "
                        "%LOCALAPPDATA%\\Keyflow. Presets, themes, the library and the practice history live in their "
                        "own files, so removing them is a separate decision.",
                        "Bấm RESET TO DEFAULT trong dock, hoặc xoá tệp visual-settings.json trong "
                        "%LOCALAPPDATA%\\Keyflow. Preset, theme, thư viện bài và lịch sử luyện tập nằm ở các tệp "
                        "riêng, nên xoá chúng là một quyết định tách biệt.")},
                {"q": T("Can I help translate it?", "Tôi có thể tham gia dịch không?"),
                 "a": T("Adding a language means adding one table of strings: the renderer, the interface and the "
                        "settings format need no change, and a static check plus the verification suite prove the new "
                        "table covers every key. Open an issue on GitHub to start.",
                        "Thêm một ngôn ngữ là thêm một bảng chuỗi: renderer, giao diện và định dạng cài đặt không "
                        "phải sửa gì, và một kiểm tra tĩnh cùng bộ kiểm chứng sẽ chứng minh bảng mới dịch đủ mọi "
                        "khoá. Hãy mở một issue trên GitHub để bắt đầu.")},
            ],
        ),

        cta(
            title=T("Everything you just read ships in one file",
                    "Mọi thứ bạn vừa đọc nằm trong một tệp duy nhất"),
            sub=T("Keyflow 1.0.0 · Windows 10 and 11, 64-bit · MIT licensed · English and Tiếng Việt.",
                  "Keyflow 1.0.0 · Windows 10 và 11, 64-bit · giấy phép MIT · English và Tiếng Việt."),
            actions=[DOWNLOAD,
                     {"label": T("Downloads & requirements", "Bản tải & yêu cầu"), "href": "download.html",
                      "kind": "btn-ghost", "icon": "download"}],
        ),
    ]
    return {
        "title": T("Guide, shortcuts & reference · Keyflow", "Hướng dẫn, phím tắt & tra cứu · Keyflow"),
        "description": T(
            "The Keyflow guide: first-time setup, getting started, every keyboard shortcut, the interface map, how "
            "the two languages work, where settings live, command-line flags, the built-in verification suite, the "
            "current limitations and the licence.",
            "Hướng dẫn Keyflow: thiết lập lần đầu, bắt đầu sử dụng, toàn bộ phím tắt, bản đồ giao diện, cách hai "
            "ngôn ngữ hoạt động, nơi lưu cài đặt, các cờ dòng lệnh, bộ kiểm chứng tích hợp, giới hạn hiện tại và "
            "giấy phép."),
        "og_image": "previews/en/shortcuts.png",
        "body": body,
    }


def _verify_card(doc) -> str:
    """The command card that sits beside the verification-suite section."""
    tk, tv = doc.key(T("Run it on the machine you just downloaded to",
                       "Chạy ngay trên máy bạn vừa tải về"))
    nk, nv = doc.key(T("Exit code 0 means pass, 1 means something failed. Every line is written as it happens, so a "
                       "crash still leaves a last line saying what it was doing.",
                       "Mã thoát 0 là đạt, 1 là có lỗi. Mỗi dòng được ghi ngay khi mục đó chạy, nên một tiến trình "
                       "bị sập vẫn để lại dòng cuối nói nó đang làm gì."))
    ck, cv = doc.key(T("Copy", "Sao chép"))
    code = ("PianoPath.exe --verify ^\n"
            "  --verify-log=%TEMP%\\keyflow-verify.log")
    return ('<div class="callout gold" style="align-items:start">' + iconbox("terminal", 20) + "<div>"
            + '<p style="margin:0 0 10px"><b data-i18n="' + tk + '">' + tv + "</b></p>"
            + '<pre class="code" id="card-verify" style="margin:0">' + code + "</pre>"
            + '<p class="muted small" style="margin:10px 0 0" data-i18n="' + nk + '">' + nv + "</p>"
            + '<button type="button" class="copy-btn" style="margin-top:10px" data-copy="card-verify" '
              'data-i18n="' + ck + '">' + cv + "</button></div></div>")


# ===========================================================================
# Download
# ===========================================================================
def build_download(doc) -> dict:
    root = doc.root
    size = lambda kind, text: {"html": '<span class="num" data-release-size="' + kind + '">' + text + "</span>"}  # noqa: E731
    link = lambda kind, label_vi, label_en, sub: {  # noqa: E731
        "link": ASSETS[kind], "asset": kind, "text": T(label_en, label_vi), "sub": sub}

    release_card = (
        '<div class="dl-card">'
        '<span class="badge" style="position:absolute;top:18px;right:18px">v<span data-release-tag>1.0.0</span></span>'
        + '<p class="eyebrow" style="margin-bottom:10px">'
        + doc.key(T("Latest release", "Bản phát hành mới nhất"))[1] + "</p>"
        + '<h2 style="font-size:clamp(24px,3vw,34px)" data-i18n="'
        + doc.key(T("Keyflow 1.0.0 · Concert Grand Edition", "Keyflow 1.0.0 · Concert Grand Edition"))[0] + '">'
        + doc.key(T("Keyflow 1.0.0 · Concert Grand Edition", "Keyflow 1.0.0 · Concert Grand Edition"))[1] + "</h2>"
        + '<p class="muted" style="margin:12px 0 18px;max-width:44ch" data-i18n="'
        + doc.key(T("Published 2 October 2026. Four packages, one checksum file, and the same application in every "
                    "one of them.",
                    "Phát hành ngày 2 tháng 10 năm 2026. Bốn gói, một tệp checksum, và cùng một ứng dụng trong mọi "
                    "gói."))[0] + '">'
        + doc.key(T("Published 2 October 2026. Four packages, one checksum file, and the same application in every "
                    "one of them.",
                    "Phát hành ngày 2 tháng 10 năm 2026. Bốn gói, một tệp checksum, và cùng một ứng dụng trong mọi "
                    "gói."))[1] + "</p>"
        + '<div class="badge-row">'
        + '<span class="badge">Windows 10 / 11 · x64</span>'
        + '<span class="badge js-date" data-release-date data-date="2026-10-02T10:10:24Z">2 Oct 2026</span>'
        + '<span class="badge">MIT</span>'
        + '<span class="badge">EN · VI</span>'
        + "</div></div>"
    )

    body = [
        pagehero(
            crumbs=[],
            crumb=T("Download", "Tải về"),
            eyebrow=T("Download", "Tải về"),
            title=T("One download, every feature", "Một bản tải, mọi tính năng"),
            lead=T("Keyflow is free and MIT licensed. Take the installer for the shortest path, or a portable ZIP if "
                   "you would rather not install anything. Every package contains the same application, the same "
                   "Yamaha grand SoundFont and the same two languages.",
                   "Keyflow miễn phí và theo giấy phép MIT. Chọn bộ cài cho nhanh, hoặc bản ZIP chạy trực tiếp nếu "
                   "bạn không muốn cài gì. Mọi gói đều chứa cùng một ứng dụng, cùng SoundFont grand Yamaha và cùng "
                   "hai ngôn ngữ."),
            chips=[
                T("Free · MIT licensed", "Miễn phí · giấy phép MIT"),
                T("No account, no sign-in", "Không tài khoản, không đăng nhập"),
                E("SHA256SUMS.txt"),
                T("Not code-signed yet", "Chưa được ký số"),
            ],
            media=release_card,
        ),

        dlhero(
            id="packages",
            eyebrow=T("Packages", "Các gói"),
            title=T("Pick the one that suits your machine", "Chọn gói hợp với máy của bạn"),
            main={
                "t": T("Installer for Windows x64", "Bộ cài cho Windows x64"),
                "file": E("Keyflow-Setup-1.0.0.exe"),
                "d": T("Start Menu and Desktop shortcuts, an uninstall entry, and a wizard in English and Tiếng "
                       "Việt. Nothing else to install: the .NET runtime is inside the package.",
                       "Shortcut ở Start Menu và Desktop, mục gỡ cài đặt, và wizard bằng cả English lẫn Tiếng Việt. "
                       "Không cần cài gì thêm: runtime .NET nằm sẵn trong gói."),
                "label": T("Download the installer", "Tải bộ cài"),
            },
            side=[
                {"t": T("Portable, self-contained", "Bản di động, self-contained"),
                 "d": T("Unzip the whole folder and run PianoPath.exe — never separate the .exe from its folder.",
                        "Giải nén cả thư mục rồi chạy PianoPath.exe — đừng tách tệp .exe ra khỏi thư mục của nó."),
                 "label": E("ZIP · x64"), "href": ASSETS["portable"], "asset": "portable"},
                {"t": T("Framework-dependent", "Bản phụ thuộc framework"),
                 "d": T("Much smaller, but the target PC needs the .NET 10 Desktop Runtime (x64).",
                        "Nhẹ hơn nhiều, nhưng máy đích cần .NET 10 Desktop Runtime (x64)."),
                 "label": T("ZIP · small", "ZIP · nhẹ"), "href": ASSETS["fd"], "asset": "fd"},
                {"t": T("Checksums", "Tệp checksum"),
                 "d": T("SHA-256 for every file in the release — the only way to be sure nothing changed on the way.",
                        "SHA-256 cho mọi tệp trong bản phát hành — cách duy nhất để chắc tệp không bị đổi trên "
                        "đường tải."),
                 "label": E("SHA256SUMS.txt"), "href": ASSETS["sums"], "asset": "sums"},
            ],
        ),

        table(
            id="all-packages",
            eyebrow=T("Everything in the release", "Mọi thứ trong bản phát hành"),
            title=T("Four packages and a checksum file", "Bốn gói và một tệp checksum"),
            head=[T("Download", "Tệp tải"), T("What it is", "Là gì"), T("Target PC needs", "Máy đích cần gì"),
                  T("Size", "Dung lượng")],
            rows=[
                [link("setup", "Bộ cài (khuyên dùng)", "Installer (recommended)",
                      "Keyflow-Setup-1.0.0.exe"),
                 T("Windows x64 installer: shortcuts, an uninstall entry, an English/Vietnamese wizard.",
                   "Bộ cài Windows x64: shortcut, mục gỡ cài đặt, wizard Anh/Việt."),
                 T("Nothing else", "Không cần gì thêm"), size("setup", "83.2 MiB")],
                [link("portable", "Bản ZIP di động", "Portable ZIP", "Keyflow-1.0.0-win-x64.zip"),
                 T("Self-contained: unzip and run PianoPath.exe.",
                   "Self-contained: giải nén là chạy PianoPath.exe."),
                 T("Nothing else", "Không cần gì thêm"), size("portable", "117.2 MiB")],
                [link("fd", "Bản phụ thuộc framework", "Framework-dependent ZIP", "Keyflow-1.0.0-win-x64-fd.zip"),
                 T("The same application, far smaller, without the bundled runtime.",
                   "Cùng ứng dụng đó, nhẹ hơn nhiều, không kèm runtime."),
                 {"html": '<a href="' + DOTNET + '" target="_blank" rel="noopener">.NET 10 Desktop Runtime (x64)</a>'},
                 size("fd", "54.9 MiB")],
                [link("arm64", "Bản Windows on ARM", "Windows on ARM ZIP", "Keyflow-1.0.0-win-arm64.zip"),
                 T("Self-contained ARM64 build, published by CI; no ARM machine has run it yet.",
                   "Bản ARM64 self-contained do CI publish; chưa máy ARM nào chạy thử."),
                 T("Nothing else", "Không cần gì thêm"), size("arm64", "105.2 MiB")],
                [link("sums", "Checksum", "Checksums", "SHA256SUMS.txt"),
                 T("SHA-256 for every file in the release.", "SHA-256 cho mọi tệp của bản phát hành."),
                 E("PowerShell Get-FileHash"),
                 {"html": '<span class="num">375 B</span>'}],
            ],
            note=T("The download buttons on this site move to the newest release by themselves when GitHub answers; "
                   "the links above are pinned to v1.0.0 so they work offline too.",
                   "Các nút tải trên trang này tự chuyển sang bản phát hành mới nhất khi GitHub trả lời; những liên "
                   "kết ở trên được ghim vào v1.0.0 nên vẫn dùng được khi ngoại tuyến."),
            actions=[{"label": T("All releases", "Tất cả bản phát hành"), "href": RELEASES,
                      "kind": "btn-ghost", "icon": "github", "external": True},
                     {"label": T("What changed in 1.0.0", "Có gì mới trong 1.0.0"), "href": "#whats-new",
                      "kind": "btn-quiet", "icon": "arrow"}],
        ),

        split(
            id="install",
            eyebrow=T("Installing", "Cài đặt"),
            title=T("Two minutes, and one folder you should not break",
                    "Hai phút, và một thư mục bạn không nên phá vỡ"),
            ticks=[
                T("Run the installer and follow the wizard — it offers English and Tiếng Việt, creates the shortcuts "
                  "and adds an uninstall entry.",
                  "Chạy bộ cài và làm theo wizard — wizard có cả English và Tiếng Việt, tạo shortcut và thêm mục "
                  "gỡ cài đặt."),
                T("Using a ZIP instead? Unzip the whole folder and run PianoPath.exe from inside it. The SoundFont "
                  "has to sit next to the executable, and the licence files travel with it.",
                  "Dùng bản ZIP? Giải nén cả thư mục rồi chạy PianoPath.exe từ bên trong. SoundFont phải nằm cạnh "
                  "tệp thực thi, và các tệp giấy phép đi kèm với nó."),
                T("Keep LICENSE.txt (MIT) and Assets\\ATTRIBUTION.txt (the SoundFont's CC BY 3.0) when you pass a "
                  "copy on to somebody else.",
                  "Hãy giữ LICENSE.txt (MIT) và Assets\\ATTRIBUTION.txt (CC BY 3.0 của SoundFont) khi bạn chia sẻ "
                  "bản sao cho người khác."),
            ],
            media=raw(
                '<div class="code-head"><span>' + doc.key(T("Inside the portable ZIP", "Bên trong bản ZIP"))[1]
                + '</span></div><pre class="code">Keyflow-1.0.0-win-x64\\\n'
                '├── PianoPath.exe              <span class="c">← '
                + doc.key(T("the single executable", "tệp thực thi duy nhất"))[1] + '</span>\n'
                '├── LICENSE.txt                <span class="c">← '
                + doc.key(T("MIT, must travel with copies", "MIT, phải đi kèm bản sao"))[1] + '</span>\n'
                '└── Assets\\\n'
                '    ├── ConcertGrand.sf2       <span class="c">← '
                + doc.key(T("the ~113 MiB SoundFont, next to the .exe", "SoundFont ~113 MiB, nằm cạnh .exe"))[1]
                + '</span>\n'
                '    └── ATTRIBUTION.txt        <span class="c">← '
                + doc.key(T("FreePats credit, CC BY 3.0", "Ghi công FreePats, CC BY 3.0"))[1] + "</span></pre>"),
        ),

        callout(
            id="smartscreen",
            style="warn",
            icon="shield",
            title=T("Windows SmartScreen will warn you once", "Windows SmartScreen sẽ cảnh báo một lần"),
            body=[
                T("The packages are not code-signed, so the first launch shows “Windows protected your PC”. Choose "
                  "More info, then Run anyway. Signing is on the project's list; until then, the checksum is how you "
                  "confirm the file you received is the file the pipeline built.",
                  "Các gói chưa được ký số nên lần chạy đầu Windows hiện “Windows protected your PC”. Chọn More "
                  "info, rồi Run anyway. Việc ký số nằm trong danh sách việc của dự án; cho tới lúc đó, checksum là "
                  "cách bạn xác nhận tệp nhận được đúng là tệp quy trình đã dựng."),
            ],
        ),

        codeblock(
            id="checksum",
            eyebrow=T("Checking a download", "Kiểm tra tệp tải về"),
            title=T("Compare the hash against SHA256SUMS.txt", "Đối chiếu hash với SHA256SUMS.txt"),
            label=E("PowerShell"),
            text=('<span class="c"># what you received</span>\n'
                  'Get-FileHash .\\Keyflow-Setup-1.0.0.exe -Algorithm SHA256\n\n'
                  '<span class="c"># what the release says it should be</span>\n'
                  'Get-Content .\\SHA256SUMS.txt'),
            note=T("The two hashes have to match exactly. A mismatch means the download was altered or truncated — "
                   "delete it and take the file from the release page again.",
                   "Hai chuỗi hash phải khớp nhau tuyệt đối. Nếu lệch nghĩa là tệp tải về đã bị thay đổi hoặc tải "
                   "dở — hãy xoá và tải lại từ trang phát hành."),
        ),

        table(
            id="requirements",
            eyebrow=T("System requirements", "Yêu cầu hệ thống"),
            title=T("What your machine needs", "Máy bạn cần gì"),
            head=[T("Component", "Thành phần"), T("Requirement", "Yêu cầu"), T("Notes", "Ghi chú")],
            rows=[
                [T("Operating system", "Hệ điều hành"),
                 T("Windows 10 (22H2 recommended) or Windows 11, 64-bit",
                   "Windows 10 (khuyến nghị 22H2) hoặc Windows 11, 64-bit"),
                 T("The app uses WPF and WinMM, so it runs on Windows only.",
                   "Ứng dụng dùng WPF và WinMM nên chỉ chạy trên Windows.")],
                [T("Running a packaged build", "Chạy bản đã đóng gói"),
                 T("Nothing extra for the self-contained builds; the framework-dependent one needs the .NET 10 "
                   "Desktop Runtime (x64)",
                   "Bản self-contained không cần gì thêm; bản framework-dependent cần .NET 10 Desktop Runtime (x64)"),
                 T("The installer and the x64/ARM64 ZIPs are self-contained.",
                   "Bộ cài và các bản ZIP x64/ARM64 đều self-contained.")],
                [T("Graphics", "Đồ hoạ"),
                 T("A GPU with Direct3D 11 (feature level 11_0 or newer, shader model 5.0)",
                   "GPU hỗ trợ Direct3D 11 (feature level 11_0 trở lên, shader model 5.0)"),
                 T("Keyflow tries the card first, then WARP — the same shaders in software — and finally the WPF "
                   "renderer, saying why in General → GRAPHICS ENGINE.",
                   "Keyflow thử card trước, rồi tới WARP — cùng shader nhưng chạy phần mềm — và cuối cùng là bộ "
                   "dựng hình WPF, kèm lý do ở General → GRAPHICS ENGINE.")],
                [T("Audio", "Âm thanh"),
                 T("Any sound card Windows recognises (waveOut output)",
                   "Bất kỳ card âm thanh nào Windows nhận (đầu ra waveOut)"),
                 T("With no output device the engine renders the audio itself, so recordings keep their full length.",
                   "Máy không có thiết bị ra âm thanh thì engine tự render phần tiếng, nên bản ghi vẫn đủ độ dài.")],
                [T("MIDI (optional)", "MIDI (tuỳ chọn)"),
                 T("A USB piano or controller Windows recognises", "Đàn hoặc thiết bị MIDI USB được Windows nhận"),
                 T("Without one you still play with the computer keyboard or the on-screen piano.",
                   "Không có đàn vẫn chơi được bằng bàn phím máy tính hoặc piano ảo.")],
                [T("Camera (optional)", "Camera (tuỳ chọn)"),
                 T("A webcam, or a video file for the overlay", "Một webcam, hoặc tệp video cho lớp phủ"),
                 T("Frames are read through Media Foundation, which Windows ships.",
                   "Khung hình được đọc qua Media Foundation, thành phần có sẵn của Windows.")],
                [T("Disk", "Ổ đĩa"),
                 T("~300 MB for a self-contained install", "~300 MB cho bản cài self-contained"),
                 T("Building from source needs about 1.5 GB for the .NET 10 SDK plus 500 MB for sources and output.",
                   "Build từ mã nguồn cần khoảng 1,5 GB cho .NET 10 SDK cộng 500 MB cho mã nguồn và bản dựng.")],
                [T("Building from source", "Build từ mã nguồn"),
                 T(".NET 10 SDK (10.0.100 or newer), Git and Git LFS",
                   ".NET 10 SDK (10.0.100 trở lên), Git và Git LFS"),
                 T("The ~113 MiB SoundFont is stored through Git LFS. Visual Studio 2026 with the .NET desktop "
                   "workload, or VS Code with the C# Dev Kit.",
                   "SoundFont ~113 MiB được lưu bằng Git LFS. Dùng Visual Studio 2026 với workload .NET desktop, "
                   "hoặc VS Code kèm C# Dev Kit.")],
            ],
        ),

        grid(
            id="whats-new",
            eyebrow=T("What is in 1.0.0", "Có gì trong bản 1.0.0"),
            title=T("The first official release", "Bản phát hành chính thức đầu tiên"),
            sub=T("One entry in the changelog describes the product as released — these are the parts a user meets "
                  "first.",
                  "Một mục trong nhật ký thay đổi mô tả sản phẩm ở trạng thái phát hành — đây là những phần người "
                  "dùng gặp đầu tiên."),
            cards=[
                {"icon": "chip", "t": T("GPU engine by default", "Engine GPU là mặc định"),
                 "d": T("A Direct3D 11 stage on its own thread with HDR, bloom and a frame-rate target up to 240 FPS; "
                        "the WPF renderer became the fallback.",
                        "Sân khấu Direct3D 11 trên luồng riêng với HDR, bloom và mục tiêu khung hình tới 240 FPS; bộ "
                        "dựng hình WPF trở thành đường dự phòng.")},
                {"icon": "piano", "t": T("Shading every frame", "Đổ bóng ở mỗi khung hình"),
                 "d": T("The 88-key keyboard is shaded in HLSL on the GPU stage, with the dock's sliders applied "
                        "per frame.",
                        "Bàn phím 88 phím được đổ bóng bằng HLSL trên sân khấu GPU, các thanh trượt của dock áp dụng "
                        "ở mỗi khung hình.")},
                {"icon": "rec", "t": T("MP4 with the sound inside", "MP4 có sẵn tiếng"),
                 "d": T("Media Foundation writes H.264 video and AAC audio into one file, with a bitrate derived from "
                        "size and frame rate.",
                        "Media Foundation ghi video H.264 và âm thanh AAC vào một tệp, bitrate tính theo kích thước "
                        "và tốc độ khung hình.")},
                {"icon": "book", "t": T("A staff layer on the stage", "Lớp khuông nhạc trên sân khấu"),
                 "d": T("Key signature inferred from the song, beaming, rests, ties, chords as one column and "
                        "hand-change curves.",
                        "Hoá biểu suy ra từ bài, nối đuôi nốt, dấu nghỉ, dấu luyến, hợp âm thành một cột và đường "
                        "cong đổi tay.")},
                {"icon": "folder", "t": T("Library, history and ghost", "Thư viện, lịch sử và bóng luyện tập"),
                 "d": T("A folder library with tags and a watcher, per-run practice history, a fourteen-day chart and "
                        "your best take drawn as a ghost.",
                        "Thư viện theo thư mục có thẻ và watcher, lịch sử luyện tập theo lượt, biểu đồ 14 ngày và "
                        "lượt chơi tốt nhất vẽ thành bóng.")},
                {"icon": "palette", "t": T("Themes you can build", "Theme bạn tự dựng được"),
                 "d": T("A theme studio deriving twenty tokens from five colours, a community preset shelf, rendered "
                        "preset thumbnails and one-line share codes.",
                        "Xưởng theme suy ra hai mươi token từ năm màu, kệ preset cộng đồng, ảnh thu nhỏ preset do "
                        "sân khấu render và mã chia sẻ một dòng.")},
                {"icon": "globe", "t": T("Two languages, checked", "Hai ngôn ngữ, được kiểm tra"),
                 "d": T("English and Tiếng Việt switch live, the dock search answers in both, and a static check "
                        "proves the tables carry the same keys.",
                        "English và Tiếng Việt đổi ngay lúc chạy, ô tìm kiếm của dock trả lời bằng cả hai, và một "
                        "kiểm tra tĩnh chứng minh hai bảng cùng tập khoá.")},
                {"icon": "shield", "t": T("Accessibility & verification", "Trợ năng & kiểm chứng"),
                 "d": T("Named glyph buttons, Tab cycling inside the dock, Windows high contrast support, and a "
                        "verification suite you can run yourself.",
                        "Nút glyph có tên, Tab xoay vòng trong dock, hỗ trợ high contrast của Windows, và bộ kiểm "
                        "chứng bạn tự chạy được.")},
                {"icon": "download", "t": T("Four packages", "Bốn gói"),
                 "d": T("An installer, a self-contained ZIP, a framework-dependent ZIP and an ARM64 ZIP, each with "
                        "SHA-256 checksums.",
                        "Một bộ cài, một ZIP self-contained, một ZIP framework-dependent và một ZIP ARM64, tất cả "
                        "kèm checksum SHA-256.")},
            ],
            actions=[{"label": T("Read the changelog", "Đọc nhật ký thay đổi"), "href": CHANGELOG,
                      "kind": "btn-ghost", "icon": "file", "external": True},
                     {"label": T("Bản tiếng Việt", "Bản tiếng Việt"), "href": CHANGELOG_VI,
                      "kind": "btn-quiet", "icon": "file", "external": True}],
        ),

        faq(
            id="faq",
            eyebrow=T("Before you install", "Trước khi cài"),
            title=T("Download questions", "Câu hỏi về bản tải"),
            items=[
                {"q": T("Which package should I take?", "Tôi nên chọn gói nào?"),
                 "a": T("The installer for a normal Windows PC — it is self-contained, so no runtime to install. Take "
                        "the portable ZIP if you prefer to keep it on a stick or in a folder of your own, the "
                        "framework-dependent ZIP if you already have the .NET 10 Desktop Runtime and want a smaller "
                        "download, and the ARM64 ZIP on Windows on ARM — knowing it has not been run on real ARM "
                        "hardware yet.",
                        "Bộ cài cho một máy Windows bình thường — bản này self-contained nên không phải cài runtime. "
                        "Chọn ZIP di động nếu bạn muốn giữ nó trong USB hoặc một thư mục riêng, chọn ZIP "
                        "framework-dependent nếu máy đã có .NET 10 Desktop Runtime và muốn tải nhẹ hơn, còn ARM64 "
                        "dành cho Windows on ARM — với lưu ý là chưa chạy thử trên máy ARM thật.")},
                {"q": T("Is it really free? Where is the catch?", "Thật sự miễn phí chứ? Có gì đánh đổi không?"),
                 "a": T("The code is MIT licensed and the packages cost nothing. There is no account, no sign-in, no "
                        "telemetry and no upsell inside the app. The bundled piano is FreePats' YDP Grand under "
                        "CC BY 3.0, credited in every package.",
                        "Mã nguồn theo giấy phép MIT và các gói hoàn toàn miễn phí. Không tài khoản, không đăng "
                        "nhập, không telemetry và không bán thêm gì trong ứng dụng. Cây đàn đi kèm là YDP Grand của "
                        "FreePats theo CC BY 3.0, được ghi công trong mỗi gói.")},
                {"q": T("Will my antivirus or Windows complain?", "Antivirus hoặc Windows có phàn nàn không?"),
                 "a": T("SmartScreen warns once because nothing is code-signed: More info → Run anyway. The release "
                        "carries SHA256SUMS.txt so you can verify the file yourself, and PianoPath.exe --verify runs "
                        "the built-in checks on your own machine and prints PASS or FAIL per subject.",
                        "SmartScreen cảnh báo một lần vì chưa có chữ ký số: More info → Run anyway. Bản phát hành "
                        "kèm SHA256SUMS.txt để bạn tự kiểm tệp, và lệnh PianoPath.exe --verify chạy các bài kiểm tra "
                        "tích hợp ngay trên máy bạn rồi in PASS hay FAIL theo từng mục.")},
                {"q": T("Does it work on an old PC with no graphics card?",
                        "Máy cũ không có card đồ hoạ thì chạy được không?"),
                 "a": T("It runs: Keyflow falls back to WARP, Windows' software rasterizer executing the same "
                        "shaders, and then to the WPF renderer if Direct3D cannot start. Expect a lower frame rate on "
                        "heavy presets — a heavy frame costs FPS, never MIDI latency.",
                        "Vẫn chạy: Keyflow lùi xuống WARP — bộ dựng hình phần mềm của Windows chạy cùng shader — rồi "
                        "tới bộ dựng hình WPF nếu Direct3D không khởi động được. Với preset nặng hãy chờ FPS thấp "
                        "hơn — khung hình nặng chỉ tốn FPS, không bao giờ làm trễ MIDI.")},
                {"q": T("Where do I report a bug?", "Báo lỗi ở đâu?"),
                 "a": T("On GitHub Issues. Attach a screenshot, the profile you exported from General → SETTINGS "
                        "PROFILE, and the log from --verify --verify-log=… — that is usually enough to reproduce it.",
                        "Trên GitHub Issues. Hãy đính kèm ảnh chụp, hồ sơ bạn xuất từ General → SETTINGS PROFILE, và "
                        "nhật ký của lệnh --verify --verify-log=… — bấy nhiêu thường là đủ để tái hiện lỗi.")},
            ],
        ),

        cta(
            title=T("Download it, plug in, and play", "Tải về, cắm đàn, và chơi"),
            sub=T("Keyflow 1.0.0 · 83.2 MiB installer · Windows 10 and 11, 64-bit · MIT licensed.",
                  "Keyflow 1.0.0 · bộ cài 83,2 MiB · Windows 10 và 11, 64-bit · giấy phép MIT."),
            actions=[{"label": T("Download the installer", "Tải bộ cài"), "href": ASSETS["setup"],
                      "kind": "btn-gold", "icon": "download", "asset": "setup", "external": True},
                     {"label": T("Portable ZIP", "Bản ZIP di động"), "href": ASSETS["portable"],
                      "kind": "btn-ghost", "icon": "folder", "asset": "portable", "external": True},
                     {"label": T("Release page", "Trang phát hành"), "href": RELEASE_PAGE,
                      "kind": "btn-quiet", "icon": "github", "external": True}],
        ),
    ]
    return {
        "title": T("Download Keyflow 1.0.0 for Windows", "Tải Keyflow 1.0.0 cho Windows"),
        "description": T(
            "Download Keyflow 1.0.0 for Windows 10 and 11, 64-bit: an 83.2 MiB installer, a portable self-contained "
            "ZIP, a smaller framework-dependent ZIP and an ARM64 build — all free, MIT licensed, with SHA-256 "
            "checksums and setup instructions.",
            "Tải Keyflow 1.0.0 cho Windows 10 và 11, 64-bit: bộ cài 83,2 MiB, bản ZIP di động self-contained, bản "
            "ZIP framework-dependent nhẹ hơn và bản ARM64 — tất cả miễn phí, giấy phép MIT, kèm checksum SHA-256 và "
            "hướng dẫn cài đặt."),
        "og_image": "previews/en/main-menu.png",
        "body": body,
    }
