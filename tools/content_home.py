#!/usr/bin/env python3
"""Content of the home page (``index.html``).

Everything here is written twice — English first, Tiếng Việt second — and the
facts come from the Keyflow release repository's README, so the marketing copy
and the documentation cannot drift apart.
"""
from __future__ import annotations

from sitekit import (ASSETS, E, ISSUES, README_EN, RELEASES, REPO, T, buttons, framed, icon,
                     iconbox, picture)
from sitekit import band, carousel, chipcloud, cta, faq, grid, hero, pagenav, raw, split, steps

PRESETS = [
    "Neon Violet", "Inferno", "Aurora Rainbow", "Ice Crystal", "Two Hands", "Classic Roll",
    "Green Screen", "Sakura Nocturne", "Concert Gold", "Moonlight Sonata", "Galaxy Voyage",
    "Electric Storm", "Ocean Depths", "Retro Arcade",
]


def _video(doc, caption: tuple[str, str], badge: tuple[str, str]) -> str:
    """The hero review video: a short branded tour of the whole product."""
    ck, cv = doc.key(caption)
    bk, bv = doc.key(badge)
    ak, av = doc.key(T("Keyflow review video: one take of the GPU stage, bookended by the new mark",
                       "Video review Keyflow: một lượt sân khấu GPU, mở và khép bằng logo mới"))
    root = doc.root
    return f"""<figure class="hero-media" style="margin:0">
<div class="frame">
<span class="frame-badge"><span class="dot"></span><span data-i18n="{bk}">{bv}</span></span>
<video controls muted loop playsinline autoplay preload="metadata" width="1080" height="608" data-poster-shot="stage-gpu-galaxy"
       poster="{root}previews/en/stage-gpu-galaxy.png"
       data-i18n-attr="aria-label={ak}" aria-label="{av}">
<source src="{root}media/showcase.mp4" type="video/mp4">
</video>
</div>
<figcaption class="frame-cap" data-i18n="{ck}">{cv}</figcaption>
</figure>"""


def build(doc) -> dict:
    """The home page spec."""
    root = doc.root
    dl = {"label": T("Download for Windows", "Tải cho Windows"), "href": "download.html",
          "kind": "btn-gold", "icon": "download"}
    gh = {"label": T("View on GitHub", "Xem trên GitHub"), "href": REPO, "kind": "btn-ghost",
          "icon": "github", "external": True}

    body = [
        hero(
            eyebrow=T("Piano visualizer & concert VFX studio",
                      "Studio trực quan hoá piano & hiệu ứng sân khấu"),
            title=T('Your MIDI, on a <em class="gold-text">concert stage</em>.',
                    'MIDI của bạn, trên một <em class="gold-text">sân khấu hoà nhạc</em>.'),
            lead=T("Keyflow plays, practises and records piano video from MIDI at production quality. "
                   "Notes fall in time, sparks glow hot and cool down, and an 88-key keyboard is lit by a "
                   "ray-traced shader — all drawn by a Direct3D 11 engine on a thread of its own, so a heavy "
                   "frame costs frame rate and never MIDI latency.",
                   "Keyflow chơi, luyện tập và quay video piano từ MIDI với chất lượng sản xuất. "
                   "Nốt nhạc rơi đúng nhịp, tia lửa nóng sáng rồi nguội dần, bàn phím 88 phím được chiếu sáng "
                   "bằng shader ray-tracing — tất cả do engine Direct3D 11 vẽ trên luồng riêng, nên một khung hình "
                   "nặng chỉ làm giảm FPS chứ không bao giờ làm trễ MIDI."),
            actions=[dl, gh],
            facts=[
                T("Free · MIT licensed", "Miễn phí · giấy phép MIT"),
                T("Windows 10 / 11, 64-bit", "Windows 10 / 11, 64-bit"),
                T("English & Tiếng Việt, switched live", "English & Tiếng Việt, đổi ngay lúc chạy"),
                T("Version 1.0.0 · Concert Grand Edition", "Phiên bản 1.0.0 · Concert Grand Edition"),
            ],
            media=_video(
                doc,
                T("The new review cut: one take of the GPU stage playing a score, bookended by the new Keyflow mark.",
                  "Bản review mới: một lượt sân khấu GPU chơi một bản nhạc, mở và khép bằng logo Keyflow mới."),
                T("Keyflow in motion", "Keyflow chuyển động"),
            ),
        ),

        band(stats=[
            (("240", "240"), T("FPS on the GPU stage", "FPS trên sân khấu GPU"), 240),
            (("16-bit", "16-bit"), T("HDR with multi-level bloom", "HDR kèm bloom nhiều tầng"), None),
            (("24,000", "24.000"), T("particles simulated at once", "hạt mô phỏng cùng lúc"), None),
            (("88", "88"), T("ray-traced keys", "phím ray-tracing"), 88),
            (("14", "14"), T("built-in stage presets", "preset sân khấu dựng sẵn"), 14),
            (("2", "2"), T("languages, no restart", "ngôn ngữ, không cần khởi động lại"), 2),
        ]),

        grid(
            id="features",
            eyebrow=T("What it does", "Làm được gì"),
            title=T("Everything a piano video needs, in one window",
                    "Mọi thứ cho một video piano, trong một cửa sổ"),
            sub=T("Six areas, one free download. Each opens on its own page with the settings, "
                  "the numbers and the pictures that belong to it.",
                  "Sáu mảng, một bản tải miễn phí. Mỗi mảng có trang riêng với đầy đủ cài đặt, "
                  "số liệu và hình ảnh của nó."),
            cards=[
                {"icon": "chip", "t": T("Direct3D 11 GPU stage", "Sân khấu GPU Direct3D 11"),
                 "d": T("Its own game loop with 16-bit HDR, multi-level bloom and up to 24,000 particles. "
                        "MIDI notes reach the synth and the engine on the callback thread itself.",
                        "Vòng lặp game riêng với HDR 16-bit, bloom nhiều tầng và tới 24.000 hạt. "
                        "Nốt MIDI đi tới bộ tổng hợp và engine ngay trên luồng callback."),
                 "href": "features/stage.html"},
                {"icon": "piano", "t": T("Ray-traced keyboard", "Bàn phím ray-tracing"),
                 "d": T("GGX lighting, a softbox with real penumbra, contact occlusion in the key gaps and "
                        "coloured light thrown back by the keys you hold.",
                        "Ánh sáng GGX, softbox có vùng nửa tối thật, che khuất tiếp xúc trong khe phím và "
                        "ánh sáng màu hắt lại từ những phím bạn giữ."),
                 "href": "features/stage.html#keyboard"},
                {"icon": "target", "t": T("Practice that listens", "Luyện tập biết lắng nghe"),
                 "d": T("Follow along, wait for your note, practise one hand, loop A-B, slow to 50% — with "
                        "accuracy, streaks, history and a ghost of your best take.",
                        "Chơi theo, chờ bạn bấm đúng nốt, tập riêng một tay, lặp A-B, giảm còn 50% — kèm "
                        "độ chính xác, chuỗi đúng, lịch sử và bóng lượt chơi tốt nhất."),
                 "href": "features/practice.html"},
                {"icon": "wave", "t": T("Your instrument, your sound", "Nhạc cụ của bạn, âm thanh của bạn"),
                 "d": T("A bundled Yamaha grand SoundFont, hall reverb, all three pedals, MIDI in and out, "
                        "and MIDI or MusicXML scores read properly.",
                        "SoundFont grand Yamaha đi kèm, reverb phòng hoà nhạc, đủ ba pedal, MIDI vào và ra, "
                        "đọc tử tế cả bản nhạc MIDI lẫn MusicXML."),
                 "href": "features/sound.html"},
                {"icon": "rec", "t": T("Record in one click", "Quay video một chạm"),
                 "d": T("MP4 (H.264 + AAC) with the sound already inside, AVI, or a 32-bit PNG sequence with "
                        "transparency for Premiere, Resolve and OBS.",
                        "MP4 (H.264 + AAC) đã có sẵn tiếng, AVI, hoặc chuỗi PNG 32-bit trong suốt cho "
                        "Premiere, Resolve và OBS."),
                 "href": "features/recording.html"},
                {"icon": "palette", "t": T("Looks you can share in one line", "Diện mạo chia sẻ bằng một dòng"),
                 "d": T("14 presets, three concert interfaces, a theme studio that derives 20 colours from five, "
                        "and a share code that carries a whole look.",
                        "14 preset, ba giao diện hoà nhạc, xưởng theme suy ra 20 màu từ năm màu gốc, "
                        "và mã chia sẻ gói trọn một diện mạo."),
                 "href": "features/design.html"},
            ],
        ),

        grid(
            cols=3,
            eyebrow=T("Also in the box", "Còn có sẵn"),
            title=T("The details that survive daily use", "Những chi tiết chịu được việc dùng mỗi ngày"),
            cards=[
                {"icon": "camera", "t": T("Camera overlay & hand tracking", "Lớp phủ camera & theo dõi bàn tay"),
                 "d": T("Put a webcam or a looping clip in any corner, key out green, and see which key your "
                        "hand is over — classical computer vision, no model to download.",
                        "Đặt webcam hoặc clip lặp ở bất kỳ góc nào, key nền xanh, và xem bàn tay đang ở phím nào — "
                        "thị giác máy tính cổ điển, không phải tải mô hình."),
                 "href": "features/camera.html"},
                {"icon": "globe", "t": T("Two languages, live", "Hai ngôn ngữ, đổi tức thì"),
                 "d": T("Switch between English and Tiếng Việt without a restart: labels, dialogs, tooltips and "
                        "error messages repaint in the current frame.",
                        "Chuyển giữa English và Tiếng Việt không cần khởi động lại: nhãn, hộp thoại, tooltip và "
                        "thông báo lỗi vẽ lại ngay trong khung hình hiện tại."),
                 "href": "guide.html#languages"},
                {"icon": "file", "t": T("Scores in, looks out", "Nhập bản nhạc, xuất phong cách"),
                 "d": T("MIDI formats 0/1/2, PPQ and SMPTE divisions, MusicXML with the hand split read from the "
                        "staves, plus a folder library with tags.",
                        "MIDI định dạng 0/1/2, độ chia PPQ và SMPTE, MusicXML với điểm chia tay đọc từ khuông nhạc, "
                        "cộng thư viện theo thư mục có gắn thẻ."),
                 "href": "features/sound.html#import"},
                {"icon": "book", "t": T("A staff layer on the stage", "Lớp khuông nhạc trên sân khấu"),
                 "d": T("Real notation over the piano roll: key signature inferred from the song, beaming by beat, "
                        "rests for the silent hand, ties across bar lines.",
                        "Ký âm thật phía trên piano roll: hoá biểu suy ra từ bài, nối đuôi theo phách, "
                        "dấu nghỉ cho tay đang im, dấu luyến vắt qua vạch nhịp."),
                 "href": "features/practice.html#sheet"},
                {"icon": "undo", "t": T("Undo, profiles, autosave", "Hoàn tác, hồ sơ, tự lưu"),
                 "d": T("32 undo states in the design dock, one file that carries stage settings plus language and "
                        "interface, and every change saves itself.",
                        "32 trạng thái hoàn tác trong bàn thiết kế, một tệp gói cả cài đặt sân khấu lẫn ngôn ngữ và "
                        "giao diện, mọi thay đổi đều tự lưu."),
                 "href": "features/design.html#profiles"},
                {"icon": "shield", "t": T("Checked by the app itself", "Do chính ứng dụng kiểm tra"),
                 "d": T("A built-in verification suite prints PASS/FAIL per subject; the product screenshots are rendered by the "
                        "app in CI, not staged mockups.",
                        "Bộ kiểm chứng tích hợp in PASS/FAIL theo từng mục; ảnh chụp sản phẩm được ứng dụng render "
                        "trong CI, không phải ảnh mockup dàn dựng."),
                 "href": "guide.html#verify"},
            ],
        ),

        split(
            id="showcase",
            eyebrow=T("The stage", "Sân khấu"),
            title=T("A concert stage that never holds up your MIDI",
                    "Sân khấu hoà nhạc không bao giờ giữ chân MIDI của bạn"),
            body=[T("The stage is a Direct3D 11 engine written on Vortice.Windows, running a game loop of its own "
                    "at 60, 120, 144, 240 FPS or unlimited. It owns the device and the context, so a heavy frame "
                    "costs frame rate — never latency. Notes arriving from MIDI are handed to the synthesizer and to "
                    "the engine on the callback thread itself, in the order they came in.",
                    "Sân khấu là một engine Direct3D 11 viết trên Vortice.Windows, chạy vòng lặp game riêng ở mức "
                    "60, 120, 144, 240 FPS hoặc không giới hạn. Engine sở hữu device và context, nên khung hình nặng "
                    "chỉ tốn FPS — không bao giờ trễ. Nốt MIDI được đưa cho bộ tổng hợp âm thanh và cho engine ngay "
                    "trên luồng callback, đúng thứ tự đã đến.")],
            ticks=[
                T("16-bit HDR, multi-level bloom and an ACES filmic tonemap",
                  "HDR 16-bit, bloom nhiều tầng và tonemap ACES filmic"),
                T("Up to 24,000 particles: incandescent sparks, plasma wisps, per-note flames, impact rings, lightning",
                  "Tới 24.000 hạt: tia lửa nóng sáng, wisp plasma, lửa theo nốt, vòng sóng va chạm, tia sét"),
                T("Seven falling-trail families, hold effects, release effects and five note morphs",
                  "Bảy họ vệt rơi, hiệu ứng giữ phím, hiệu ứng nhả phím và năm kiểu biến hình nốt"),
                T("Six GPU shader backgrounds and six hit-line motion styles, each with its own intensity and speed",
                  "Sáu nền shader GPU và sáu kiểu chuyển động đường chạm, mỗi thứ có thanh chỉnh riêng"),
                T("If Direct3D cannot start, the WPF renderer takes over and General says why",
                  "Nếu Direct3D không khởi động được, bộ dựng hình WPF thay thế và trang General nói rõ lý do"),
            ],
            actions=[{"label": T("Inside the GPU stage", "Tìm hiểu sân khấu GPU"),
                      "href": "features/stage.html", "kind": "btn-ghost", "icon": "arrow"}],
            media=framed(doc, "stage-gpu-galaxy",
                          T("Galaxy Voyage preset on the GPU stage", "Preset Galaxy Voyage trên sân khấu GPU"),
                          T("Galaxy Voyage: rainbow trails over a cosmic ambient layer",
                            "Galaxy Voyage: vệt cầu vồng trên lớp nền vũ trụ"),
                          badge=T("GPU stage · Galaxy Voyage", "Sân khấu GPU · Galaxy Voyage"), lazy=False),
        ),

        split(
            id="keyboard",
            flip=True,
            eyebrow=T("The keyboard", "Bàn phím"),
            title=T("Eighty-eight keys, shaded like a product render",
                    "Tám mươi tám phím, đổ bóng như một bức render sản phẩm"),
            body=[T("The keyboard is not a picture: it is a shader. A Cook-Torrance GGX BRDF with Smith visibility "
                    "and Schlick fresnel, a softbox with a real penumbra, contact occlusion inside the gaps between "
                    "keys, image-based lighting from the environment, coloured light thrown back by the keys that "
                    "are sounding, and an ACES filmic tonemap.",
                    "Bàn phím không phải là một bức ảnh: nó là một shader. BRDF Cook-Torrance GGX với Smith "
                    "visibility và Schlick fresnel, softbox có vùng nửa tối thật, che khuất tiếp xúc trong khe giữa "
                    "các phím, ánh sáng môi trường IBL, ánh sáng màu hắt lại từ những phím đang kêu, và tonemap "
                    "ACES filmic.")],
            ticks=[
                T("Classic, Studio 3D or Glass keys, with key labels, lid shadow, red felt strip and key dip",
                  "Phím kiểu Classic, Studio 3D hoặc Glass, kèm nhãn phím, bóng nắp đàn, dải nỉ đỏ và độ lún khi nhấn"),
                T("Off / Fast / Balanced / Cinematic quality, plus key light, gloss, rim, emission, exposure and camera tilt",
                  "Bốn mức chất lượng Off / Fast / Balanced / Cinematic, cùng đèn chính, độ bóng, viền, phát sáng, phơi sáng và nghiêng camera"),
                T("On the GPU stage every slider goes straight into HLSL and is re-applied each frame",
                  "Trên sân khấu GPU, mọi thanh trượt đi thẳng vào HLSL và được áp lại ở mỗi khung hình"),
                T("Keys of sounding MIDI notes light up too, not only the keys you press",
                  "Phím của nốt MIDI đang phát cũng sáng, không chỉ phím bạn bấm"),
            ],
            actions=[{"label": T("How the shading works", "Cách đổ bóng hoạt động"),
                      "href": "features/stage.html#keyboard", "kind": "btn-ghost", "icon": "arrow"}],
            media=framed(doc, "stage-gpu",
                          T("Neon Violet, the default stage look", "Neon Violet, diện mạo sân khấu mặc định"),
                          T("Neon Violet, the default look: a held chord joins the keys with hold effects",
                            "Neon Violet, diện mạo mặc định: một hợp âm đang giữ nối các phím bằng hiệu ứng giữ"),
                          badge=T("GPU stage · Neon Violet", "Sân khấu GPU · Neon Violet")),
        ),

        split(
            id="practice",
            eyebrow=T("Practice mode", "Chế độ luyện tập"),
            title=T("Learn a piece note by note, and keep the evidence",
                    "Học một bản nhạc từng nốt một, và giữ lại bằng chứng"),
            ticks=[
                T("Follow along, Wait for my note, Right hand only, Left hand only — the score waits for the right note",
                  "Chơi theo, Chờ nốt của tôi, Chỉ tay phải, Chỉ tay trái — bản nhạc chờ bạn bấm đúng nốt"),
                T("A-B loop any passage, tempo 50–150%, and an automatic practice tempo that slows down when you miss",
                  "Lặp A-B bất kỳ đoạn nào, tempo 50–150%, cùng tempo luyện tập tự động chậm lại khi bạn sai"),
                T("Accuracy, streak and timing feedback live under the stage, scored per run",
                  "Độ chính xác, chuỗi đúng liên tiếp và nhận xét nhịp ngay dưới sân khấu, chấm theo từng lượt"),
                T("History keeps every run, draws a fourteen-day chart and overlays your best take as a ghost",
                  "Lịch sử giữ mọi lượt chơi, vẽ biểu đồ 14 ngày và phủ lượt tốt nhất lên thành bóng"),
                T("The hand split comes from the MusicXML staves, or is inferred from how the notes spread",
                  "Điểm chia tay đọc từ khuông MusicXML, hoặc tự suy ra theo cách nốt trải trên bàn phím"),
            ],
            actions=[{"label": T("Open practice mode", "Xem chế độ luyện tập"),
                      "href": "features/practice.html", "kind": "btn-ghost", "icon": "arrow"}],
            media=framed(doc, "practice-dock",
                          T("The Practice page of the settings dock", "Trang Practice của bàn cài đặt"),
                          T("Practice: modes, tempo and the A-B loop",
                            "Luyện tập: chế độ tập, tempo và vòng lặp A-B"),
                          badge=T("Practice page", "Trang luyện tập")),
        ),

        split(
            id="recording",
            flip=True,
            eyebrow=T("Recording", "Ghi hình"),
            title=T("Press REC, and the video already has the sound",
                    "Bấm REC, và video đã có sẵn tiếng"),
            ticks=[
                T("MP4 (H.264 + AAC) written by Windows' own Media Foundation — no ffmpeg, no extra library",
                  "MP4 (H.264 + AAC) ghi bằng Media Foundation của chính Windows — không ffmpeg, không thư viện ngoài"),
                T("AVI plus a 16-bit stereo WAV beside it, with the exact ffmpeg line printed for you",
                  "AVI kèm tệp WAV stereo 16-bit ngay cạnh, và in sẵn đúng dòng lệnh ffmpeg để ghép"),
                T("A 32-bit PNG sequence with real transparency, for compositing in Premiere, Resolve or OBS",
                  "Chuỗi PNG 32-bit trong suốt thật, để ghép hậu kỳ trong Premiere, Resolve hoặc OBS"),
                T("Window, 720p or 1080p at 15–60 fps, taken from an off-screen frame at the recording's own size",
                  "Theo cửa sổ, 720p hoặc 1080p ở 15–60 fps, lấy từ khung off-screen đúng kích thước bản ghi"),
                T("The Green Screen preset paints a pure green backdrop so OBS can key it out",
                  "Preset Green Screen tô nền xanh lá thuần để OBS key ra"),
            ],
            actions=[{"label": T("Formats and pipelines", "Định dạng và quy trình"),
                      "href": "features/recording.html", "kind": "btn-ghost", "icon": "arrow"}],
            media=framed(doc, "recording-dock",
                          T("The Recording page: format, resolution and frame rate",
                            "Trang Recording: định dạng, độ phân giải và tốc độ khung hình"),
                          T("Recording: MP4, AVI or PNG with alpha — plus the audio track",
                            "Ghi hình: MP4, AVI hoặc PNG trong suốt — kèm đường tiếng"),
                          badge=T("Recording page", "Trang ghi hình")),
        ),

        chipcloud(
            id="presets",
            eyebrow=T("Presets", "Preset"),
            title=T("Fourteen looks, ready before you touch a slider",
                    "Mười bốn diện mạo, sẵn sàng trước khi bạn chạm vào thanh trượt"),
            sub=T("Every preset also suggests the concert interface that suits it, and each one is rendered by both "
                  "engines side by side in CI so the GPU stage keeps the theme's intent.",
                  "Mỗi preset còn gợi ý giao diện hoà nhạc hợp với nó, và được render bằng cả hai engine đặt cạnh "
                  "nhau trong CI để sân khấu GPU giữ đúng ý đồ của chủ đề."),
            items=[E(name) for name in PRESETS],
            actions=[
                {"label": T("See all presets side by side", "Xem tất cả preset cạnh nhau"),
                 "href": "gallery.html#presets", "kind": "btn-ghost", "icon": "grid"},
                {"label": T("Presets, themes & share codes", "Preset, theme & mã chia sẻ"),
                 "href": "features/design.html", "kind": "btn-quiet", "icon": "palette"},
            ],
        ),

        carousel(
            id="screens",
            interval=6000,
            label=T("Keyflow screenshots", "Ảnh chụp Keyflow"),
            eyebrow=T("Gallery", "Hình ảnh"),
            title=T("Rendered by the application itself", "Do chính ứng dụng render"),
            sub=T("These app screenshots are captured by Keyflow in CI with <code>--snapshot</code> — one set per language, "
                  "updated whenever the interface changes.",
                  "Các ảnh chụp ứng dụng này được Keyflow tạo trong CI bằng <code>--snapshot</code> — mỗi ngôn ngữ "
                  "một bộ, cập nhật khi giao diện thay đổi."),
            slides=[
                {"shot": "stage-gpu-galaxy", "cap": T("Galaxy Voyage: rainbow trails over a cosmic layer",
                                                      "Galaxy Voyage: vệt cầu vồng trên nền vũ trụ")},
                {"shot": "stage-gpu-storm", "cap": T("Electric Storm: speed lines and arcs between held keys",
                                                     "Electric Storm: vệt tốc độ và tia điện giữa các phím đang giữ")},
                {"shot": "stage-live", "cap": T("The live stage: falling notes, hit line, sparks and the transport bar",
                                                "Sân khấu live: nốt rơi, đường chạm, tia lửa và thanh transport")},
                {"shot": "background-image", "cap": T("Your own picture behind the keys, centre-cropped and dimmed",
                                                      "Ảnh của bạn sau bàn phím, cắt giữa và được làm tối")},
                {"shot": "main-menu", "cap": T("The Concert Grand start menu, with the language chips",
                                               "Menu khởi động Concert Grand, kèm chip chọn ngôn ngữ")},
                {"shot": "design-dock", "cap": T("Stage design dock: presets and every layer of the stage",
                                                 "Bàn thiết kế sân khấu: preset và mọi lớp hiệu ứng")},
                {"shot": "theme-dock", "cap": T("Three concert interfaces, plus the themes you make yourself",
                                                "Ba giao diện hoà nhạc, cùng theme bạn tự tạo")},
                {"shot": "history-dock", "cap": T("Practice history: every run of the open song",
                                                  "Lịch sử luyện tập: mọi lượt chơi của bài đang mở")},
            ],
            actions=[{"label": T("Open the full gallery", "Mở thư viện ảnh đầy đủ"),
                      "href": "gallery.html", "kind": "btn-ghost", "icon": "image"}],
        ),

        steps(
            id="start",
            eyebrow=T("Get started", "Bắt đầu"),
            title=T("Up and playing in a minute", "Chơi được ngay trong một phút"),
            items=[
                {"t": T("Download", "Tải về"),
                 "d": T("Take the installer (recommended) or the portable ZIP from the latest release — "
                        "nothing else to install for the self-contained build.",
                        "Lấy bộ cài (khuyên dùng) hoặc bản ZIP chạy trực tiếp ở bản phát hành mới nhất — "
                        "bản self-contained không cần cài thêm gì.")},
                {"t": T("Plug in, or just type", "Cắm đàn, hoặc gõ phím"),
                 "d": T("Connect a MIDI keyboard and Keyflow finds it, or play "
                        "A W S E D F T G Y H U J K on the computer keyboard.",
                        "Cắm đàn MIDI để Keyflow tự nhận, hoặc chơi "
                        "A W S E D F T G Y H U J K ngay trên bàn phím máy tính.")},
                {"t": T("Pick a look and press REC", "Chọn diện mạo rồi bấm REC"),
                 "d": T("Choose a preset in Settings → Style, an interface in Theme, then record an MP4 "
                        "with the sound already inside.",
                        "Chọn preset ở Settings → Style, giao diện ở Theme, rồi quay một tệp MP4 "
                        "đã có sẵn tiếng.")},
            ],
            note=T("Not code-signed yet: the first launch may show Windows SmartScreen — choose “More info”, "
                   "then “Run anyway”. Every release also ships SHA256SUMS.txt.",
                   "Ứng dụng chưa được ký số: lần chạy đầu Windows SmartScreen có thể cảnh báo — chọn “More info”, "
                   "rồi “Run anyway”. Mỗi bản phát hành đều kèm SHA256SUMS.txt."),
        ),

        split(
            id="languages",
            eyebrow=T("Two languages", "Hai ngôn ngữ"),
            title=T("English and Tiếng Việt, repainted in the same frame",
                    "English và Tiếng Việt, vẽ lại trong cùng một khung hình"),
            ticks=[
                T("Switch on the General page or with the chips on the start menu — no restart, no half-translated window",
                  "Đổi ở trang General hoặc bằng chip ngay trên menu khởi động — không khởi động lại, không giao diện nửa dịch"),
                T("The dock search answers in both languages and in synonyms: “speed”, “tốc độ”, “fps” and “tempo” "
                  "all land on the same slider",
                  "Ô tìm kiếm của bàn cài đặt trả lời bằng cả hai ngôn ngữ và cả từ đồng nghĩa: “speed”, “tốc độ”, "
                  "“fps” và “tempo” đều ra cùng một thanh trượt"),
                T("Ids never change: preset names, theme ids, device names and saved files stay English, so a "
                  "profile travels between machines",
                  "Id không bao giờ đổi: tên preset, id theme, tên thiết bị và tệp đã lưu vẫn là tiếng Anh, "
                  "nên hồ sơ mang sang máy khác vẫn đọc được"),
                T("A missing translation prints English rather than an empty box, and a static check proves both "
                  "tables carry the same keys",
                  "Thiếu bản dịch thì in tiếng Anh chứ không in ô trống, và một kiểm tra tĩnh chứng minh hai bảng "
                  "cùng tập khoá"),
            ],
            actions=[{"label": T("Languages, files and command line", "Ngôn ngữ, tệp và dòng lệnh"),
                      "href": "guide.html#languages", "kind": "btn-ghost", "icon": "arrow"}],
            media=framed(doc, "language-dock",
                          T("The General page running in Vietnamese", "Trang General khi chạy bằng tiếng Việt"),
                          T("The General page in Vietnamese: language, graphics engine and settings profile",
                            "Trang General tiếng Việt: ngôn ngữ, engine đồ hoạ và hồ sơ cài đặt"),
                          badge=T("Tiếng Việt", "Tiếng Việt")),
        ),

        faq(
            id="faq",
            eyebrow=T("Questions", "Câu hỏi"),
            title=T("Before you download", "Trước khi tải về"),
            items=[
                {"q": T("Is Keyflow really free?", "Keyflow có thật sự miễn phí không?"),
                 "a": T("Yes. The application is free and the code is released under the MIT licence; the bundled "
                        "SoundFont belongs to FreePats under CC BY 3.0. There is no account, no subscription and "
                        "no telemetry.",
                        "Có. Ứng dụng miễn phí và mã nguồn phát hành theo giấy phép MIT; SoundFont đi kèm thuộc về "
                        "FreePats theo CC BY 3.0. Không tài khoản, không phí thuê bao và không telemetry.")},
                {"q": T("Which computers can run it?", "Máy nào chạy được?"),
                 "a": T("Windows 10 (22H2 recommended) or Windows 11, 64-bit, with a Direct3D 11 GPU "
                        "(feature level 11_0, shader model 5.0). Machines without a compatible card fall back to "
                        "WARP — the same shaders, slower — and then to the WPF renderer. A Windows-on-ARM package "
                        "is published but has not been run on real ARM hardware yet.",
                        "Windows 10 (khuyến nghị 22H2) hoặc Windows 11, 64-bit, với GPU Direct3D 11 "
                        "(feature level 11_0, shader model 5.0). Máy không có card tương thích sẽ lùi xuống WARP — "
                        "cùng shader, chỉ chậm hơn — rồi tới bộ dựng hình WPF. Bản Windows-on-ARM đã được phát hành "
                        "nhưng chưa chạy thử trên máy ARM thật.")},
                {"q": T("Do I need a MIDI keyboard?", "Có bắt buộc phải có đàn MIDI không?"),
                 "a": T("No. The computer keyboard plays one octave from middle C, the on-screen piano takes mouse "
                        "clicks with full colour and spark response, and any USB instrument Windows recognises "
                        "works with velocity, note off and all three pedals.",
                        "Không. Bàn phím máy tính chơi được một quãng tám từ nốt C giữa, piano trên màn hình nhận "
                        "click chuột với đầy đủ phản hồi màu và tia lửa, còn bất kỳ đàn USB nào Windows nhận ra "
                        "đều dùng được velocity, note off và cả ba pedal.")},
                {"q": T("Does the recorded MP4 contain the audio?", "Tệp MP4 quay ra có chứa tiếng không?"),
                 "a": T("Yes — H.264 video and AAC audio in one file, written by the Media Foundation encoder that "
                        "ships with Windows. If a machine has no AAC encoder the take keeps the picture and the "
                        "dialog says why; AVI always writes a WAV beside it instead.",
                        "Có — video H.264 và âm thanh AAC trong cùng một tệp, ghi bằng bộ mã hoá Media Foundation "
                        "có sẵn trong Windows. Máy nào thiếu bộ mã hoá AAC thì bản ghi vẫn có hình và hộp thoại nói "
                        "rõ lý do; còn AVI luôn ghi kèm một tệp WAV bên cạnh.")},
                {"q": T("Why does Windows warn me the first time?", "Vì sao Windows cảnh báo ở lần chạy đầu?"),
                 "a": T("The packages are not code-signed, so SmartScreen shows “Windows protected your PC”. "
                        "Choose More info, then Run anyway — and compare the file against SHA256SUMS.txt from the "
                        "release if you want to be sure nothing changed on the way.",
                        "Các gói chưa được ký số nên SmartScreen hiện “Windows protected your PC”. "
                        "Chọn More info rồi Run anyway — và đối chiếu tệp với SHA256SUMS.txt của bản phát hành "
                        "nếu bạn muốn chắc chắn tệp không bị thay đổi trên đường tải.")},
                {"q": T("Can I use my own piano sound?", "Tôi dùng âm thanh piano của riêng mình được không?"),
                 "a": T("Yes. Open Settings → Audio → Load SoundFont and pick any uncompressed .sf2, then choose a "
                        "bank/program preset and toggle the hall reverb. .sf3 is not supported yet.",
                        "Được. Mở Settings → Audio → Load SoundFont và chọn bất kỳ tệp .sf2 không nén nào, sau đó "
                        "chọn preset bank/program và bật/tắt hall reverb. Định dạng .sf3 chưa được hỗ trợ.")},
            ],
        ),

        cta(
            title=T("Put your music on stage", "Đưa âm nhạc của bạn lên sân khấu"),
            sub=T("One download, every feature, two languages. Keyflow 1.0.0 for Windows 10 and 11.",
                  "Một bản tải, mọi tính năng, hai ngôn ngữ. Keyflow 1.0.0 cho Windows 10 và 11."),
            actions=[dl, gh,
                     {"label": T("Read the guide", "Đọc hướng dẫn"), "href": "guide.html",
                      "kind": "btn-quiet", "icon": "book"}],
        ),
    ]

    return {
        "title": T("Keyflow · Piano Visualizer & Concert VFX Studio for Windows",
                   "Keyflow · Studio trực quan hoá piano & hiệu ứng sân khấu cho Windows"),
        "description": T(
            "Keyflow turns MIDI into concert-grade piano performances and videos: a Direct3D 11 GPU stage, "
            "a ray-traced 88-key keyboard, practice modes and one-click MP4 recording. Free for Windows 10 and 11, "
            "in English and Tiếng Việt.",
            "Keyflow biến MIDI thành buổi biểu diễn và video piano chất lượng hoà nhạc: sân khấu GPU Direct3D 11, "
            "bàn phím 88 phím ray-tracing, các chế độ luyện tập và quay MP4 một chạm. Miễn phí cho Windows 10 và 11, "
            "có English và Tiếng Việt."),
        "og_image": "previews/en/stage-gpu-galaxy.png",
        "body": body,
    }
