#!/usr/bin/env python3
"""Feature pages, part two: recording, the design dock, and camera & hands."""
from __future__ import annotations

from sitekit import (E, T, band, callout, chipcloud, codeblock, cta, framed, grid, groups,
                     iconbox, pagehero, pagenav, split, specdl, steps, table)

DOWNLOAD = {"label": T("Download for Windows", "Tải cho Windows"), "href": "download.html",
            "kind": "btn-gold", "icon": "download"}
TRAIL = [("Features", "index.html#features")]


def _codecard(doc, icon_name, title, code, note):
    """A small card with a copyable command — used where a picture would say less."""
    tk, tv = doc.key(title)
    nk, nv = doc.key(note)
    ck, cv = doc.key(T("Copy", "Sao chép"))
    return (
        '<div class="callout gold" style="align-items:start">' + iconbox(icon_name, 20) + "<div>"
        + '<p style="margin:0 0 10px"><b data-i18n="' + tk + '">' + tv + "</b></p>"
        + '<pre class="code" id="card-' + icon_name + '" style="margin:0">' + code + "</pre>"
        + '<p class="muted small" style="margin:10px 0 0" data-i18n="' + nk + '">' + nv + "</p>"
        + '<button type="button" class="copy-btn" style="margin-top:10px" data-copy="card-' + icon_name
        + '" data-i18n="' + ck + '">' + cv + "</button>"
        + "</div></div>"
    )


def feature_hero(doc, *, crumb, eyebrow, title, lead, chips, shot, alt, cap, badge=None):
    return pagehero(
        crumbs=[(T("Features", "Tính năng"), "index.html#features")],
        crumb=crumb, eyebrow=eyebrow, title=title, lead=lead,
        chips=[(c, "gold") for c in chips],
        actions=[DOWNLOAD,
                 {"label": T("All features", "Tất cả tính năng"), "href": "index.html#features",
                  "kind": "btn-ghost", "icon": "grid"}],
        media=framed(doc, shot, alt, cap, badge=badge, lazy=False),
    )


# ===========================================================================
# 4. Recording & export
# ===========================================================================
def build_recording(doc) -> dict:
    body = [
        feature_hero(
            doc,
            crumb=T("Recording & export", "Ghi hình & xuất bản"),
            eyebrow=T("Recording", "Ghi hình"),
            title=T("Press REC, and the video already has the sound",
                    "Bấm REC, và video đã có sẵn tiếng"),
            lead=T("Three ways out of the stage: an MP4 with H.264 video and AAC audio in one file, an AVI with a "
                   "WAV beside it, or a 32-bit PNG sequence with real transparency for compositing. Resolution and "
                   "frame rate are yours, and the recording is drawn at its own size — not upscaled from the "
                   "preview.",
                   "Ba đường ra khỏi sân khấu: một tệp MP4 gồm video H.264 và âm thanh AAC, một tệp AVI kèm WAV bên "
                   "cạnh, hoặc chuỗi PNG 32-bit trong suốt thật để ghép hậu kỳ. Độ phân giải và tốc độ khung hình "
                   "do bạn chọn, và bản ghi được vẽ ở đúng kích thước của nó — không phải phóng to từ khung xem trước."),
            chips=[
                E("MP4 · H.264 + AAC"), E("AVI + WAV"), E("PNG 32-bit alpha"),
                T("Window / 720p / 1080p", "Theo cửa sổ / 720p / 1080p"),
                E("15–60 fps"),
            ],
            shot="recording-dock",
            alt=T("The Recording page: format, resolution, frame rate, audio and transparency",
                  "Trang Recording: định dạng, độ phân giải, tốc độ khung hình, âm thanh và nền trong suốt"),
            cap=T("The OUTPUT card of the Recording page: everything here applies from the next take.",
                  "Thẻ OUTPUT của trang Recording: mọi lựa chọn ở đây áp dụng từ lần ghi kế tiếp."),
            badge=T("Session · Recording", "Phiên · Ghi hình"),
        ),

        band(stats=[
            (("3", "3"), T("output formats", "định dạng xuất"), 3),
            (("1080p", "1080p"), T("maximum resolution", "độ phân giải tối đa"), None),
            (("60", "60"), T("frames per second, maximum", "khung hình mỗi giây, tối đa"), 60),
            (("2–24 Mbps", "2–24 Mbps"), T("H.264 bitrate range", "dải bitrate H.264"), None),
        ]),

        table(
            id="formats",
            eyebrow=T("Formats", "Định dạng"),
            title=T("Which one to pick, and what your PC needs", "Chọn định dạng nào, và máy bạn cần gì"),
            head=[T("Format", "Định dạng"), T("What you get", "Bạn nhận được gì"),
                  T("What the PC needs", "Máy cần gì"), T("Best for", "Hợp với")],
            rows=[
                [E("MP4 (H.264 + AAC)"),
                 T("One file with the picture and the sound already inside it; each audio sample carries its own "
                   "timestamp, so nothing drifts.",
                   "Một tệp có cả hình lẫn tiếng bên trong; mỗi mẫu âm thanh mang đúng mốc thời gian của nó nên "
                   "không lệch."),
                 T("Windows' own Media Foundation encoders — H.264 and AAC. Nothing to install.",
                   "Bộ mã hoá Media Foundation của chính Windows — H.264 và AAC. Không phải cài gì."),
                 T("YouTube, TikTok, sending a take to somebody.",
                   "Đăng YouTube, TikTok, gửi bản quay cho người khác.")],
                [E("AVI video"),
                 T("The picture in one file plus a 16-bit stereo WAV beside it (take.wav), and the exact ffmpeg line "
                   "printed for you after you stop.",
                   "Phần hình trong một tệp, kèm tệp WAV stereo 16-bit bên cạnh (take.wav), và in sẵn đúng dòng "
                   "lệnh ffmpeg sau khi bạn dừng ghi."),
                 T("An MJPEG codec (for example the K-Lite pack) if you want smaller files — optional; without one "
                   "the AVI is uncompressed RGB and stops at the 2 GB AVI limit.",
                   "Một codec MJPEG (ví dụ gói K-Lite) nếu muốn tệp nhỏ hơn — không bắt buộc; nếu không có, AVI sẽ "
                   "là RGB không nén và tự dừng ở giới hạn 2 GB."),
                 T("Editing suites that want an intermediate file.",
                   "Các phần mềm dựng phim cần một tệp trung gian.")],
                [T("PNG sequence (32-bit alpha)", "Chuỗi PNG (32-bit alpha)"),
                 T("A folder of frame-000001.png files with a real alpha channel, plus sequence.json recording the "
                   "size, the frame rate, the frame count and the ffmpeg command that rebuilds an alpha video.",
                   "Một thư mục các tệp frame-000001.png có kênh alpha thật, kèm sequence.json ghi kích thước, tốc "
                   "độ khung hình, số khung và dòng lệnh ffmpeg dựng lại thành video alpha."),
                 T("Nothing extra; this path is drawn by the software renderer so transparency is exact.",
                   "Không cần gì thêm; đường này do bộ dựng hình phần mềm vẽ nên độ trong suốt là chính xác."),
                 T("Compositing over your own footage in Premiere, Resolve or OBS.",
                   "Ghép đè lên cảnh quay của bạn trong Premiere, Resolve hoặc OBS.")],
            ],
            note=T("Format, resolution, frame rate, the audio track and transparency live in the OUTPUT card of the "
                   "Recording page and apply from the next take.",
                   "Định dạng, độ phân giải, tốc độ khung hình, đường tiếng và nền trong suốt nằm ở thẻ OUTPUT của "
                   "trang Recording và áp dụng từ lần ghi kế tiếp."),
        ),

        split(
            id="mp4",
            eyebrow=T("MP4 in one file", "MP4 trong một tệp"),
            title=T("Written by Windows itself — no ffmpeg, no extra library",
                    "Do chính Windows viết ra — không ffmpeg, không thư viện ngoài"),
            ticks=[
                T("A Media Foundation sink writer takes the stage frames, converts them to NV12 (BT.601) and encodes "
                  "H.264 with a bitrate computed from size × fps — a 2 Mbps floor and a 24 Mbps ceiling.",
                  "Media Foundation sink writer nhận khung hình sân khấu, chuyển sang NV12 (BT.601) và mã hoá "
                  "H.264 với bitrate tính theo kích thước × fps — sàn 2 Mbps, trần 24 Mbps."),
                T("The engine's PCM is encoded to AAC into the same file, and every sample keeps its own timestamp, "
                  "so picture and sound cannot drift apart.",
                  "PCM của engine được mã hoá AAC vào cùng tệp, và mỗi mẫu giữ đúng mốc thời gian của nó, nên hình "
                  "và tiếng không thể lệch nhau."),
                T("A machine with no H.264 encoder gets a clear sentence with the error code instead of a broken "
                  "file; one with H.264 but no AAC encoder still records the picture, and the dialog says why the "
                  "sound is missing.",
                  "Máy không có bộ mã hoá H.264 sẽ nhận một câu báo rõ kèm mã lỗi thay vì một tệp hỏng; máy có "
                  "H.264 nhưng thiếu bộ mã hoá AAC vẫn ghi được phần hình, và hộp thoại nói rõ vì sao thiếu tiếng."),
                T("No piano loaded means picture only, and the status line says so before you press REC.",
                  "Chưa tải cây đàn thì chỉ ghi hình, và dòng thông tin nói rõ trước khi bạn bấm REC."),
            ],
            media=framed(doc, "recording-dock",
                         T("The Recording page of the settings dock", "Trang Recording của bàn cài đặt"),
                         T("Recording → OUTPUT: format, resolution, frame rate, Record audio and Transparent "
                           "background.",
                           "Recording → OUTPUT: định dạng, độ phân giải, tốc độ khung hình, Record audio và "
                           "Transparent background."),
                         badge=T("OUTPUT card", "Thẻ OUTPUT")),
        ),

        split(
            id="audio",
            flip=True,
            eyebrow=T("The audio track", "Đường tiếng"),
            title=T("The same samples you hear, captured while you play",
                    "Đúng những mẫu âm bạn nghe, được lấy ngay lúc chơi"),
            ticks=[
                T("Record audio is on by default. The tap takes the very PCM blocks the render engine plays, and it "
                  "is attached only while a recording runs — performing normally costs nothing.",
                  "Record audio mặc định bật. Tap lấy đúng những khối PCM mà engine render phát, và chỉ được gắn "
                  "trong lúc ghi — lúc diễn bình thường không tốn gì."),
                T("AVI and PNG sequences get a 16-bit stereo 44.1 kHz WAV beside the video: take.wav, or audio.wav "
                  "inside the frame folder.",
                  "AVI và chuỗi PNG có một tệp WAV stereo 16-bit 44,1 kHz nằm cạnh video: take.wav, hoặc audio.wav "
                  "trong thư mục khung hình."),
                T("A machine with no audio output device is not a problem: the engine renders the audio itself, so "
                  "the take still has its full length.",
                  "Máy không có thiết bị ra âm thanh cũng không sao: engine tự render phần tiếng, nên bản ghi vẫn "
                  "đủ độ dài."),
                T("After you stop, the dialog prints the length and the ffmpeg line that muxes the two files into "
                  "one MP4.",
                  "Sau khi dừng ghi, hộp thoại in độ dài cùng dòng lệnh ffmpeg ghép hai tệp thành một MP4."),
                T("The info line adapts to the machine: with Salamander loaded it says where the sound goes, without "
                  "it it says plainly that the take will be silent.",
                  "Dòng thông tin đổi theo thực tế từng máy: đã nạp Salamander thì nói rõ đường tiếng đi đâu, chưa "
                  "có thì nói thẳng rằng bản ghi sẽ không có tiếng."),
            ],
            media=_codecard(
                doc, "wave",
                T("The line the dialog prints", "Dòng lệnh hộp thoại in ra"),
                "ffmpeg -i video.avi -i take.wav \\\n       -c:v copy -c:a aac take.mp4",
                T("Copy it, run it, and the AVI plus its WAV become one MP4 — the video stream is copied, not "
                  "re-encoded.",
                  "Chép lại, chạy, và tệp AVI cùng WAV của nó thành một MP4 — luồng video được copy chứ không mã "
                  "hoá lại."),
            ),
        ),

        split(
            id="gpu-take",
            eyebrow=T("Recording from the GPU stage", "Ghi hình từ sân khấu GPU"),
            title=T("An extra off-screen frame, at exactly the recording's size",
                    "Một khung off-screen vẽ thêm, đúng kích thước bản ghi"),
            body=[T("While the GPU stage is up, REC makes the render loop draw one more frame off-screen at exactly "
                    "the resolution and frame rate of the recording — not an upscaled copy of the preview window. "
                    "The WPF layers (the staff, the camera picture, the counters) are composited on top of it.",
                    "Khi sân khấu GPU đang hiện, REC khiến luồng dựng hình vẽ thêm một khung off-screen đúng kích "
                    "thước và tốc độ khung hình của bản ghi — không phải bản phóng to của khung xem trước. Các lớp "
                    "WPF (khuông nhạc, hình camera, bộ đếm) được trộn lên trên.")],
            ticks=[
                T("The render loop alone — no window, no preview — still hands over exact-size frames, which is what "
                  "the built-in verification suite checks.",
                  "Chỉ riêng luồng dựng hình — không cửa sổ, không xem trước — vẫn đưa ra khung đúng kích thước, "
                  "và đó là điều bộ kiểm chứng tích hợp kiểm tra."),
                T("Transparent PNG keeps using the software renderer, because that is the path that can produce a "
                  "real alpha channel.",
                  "Bản PNG trong suốt vẫn dùng bộ dựng hình phần mềm, vì đó là đường vẽ ra được kênh alpha thật."),
                T("The Green Screen preset paints a pure green backdrop, which is exactly the colour the camera "
                  "overlay keys out — so OBS can key the stage too.",
                  "Preset Green Screen tô nền xanh lá thuần, đúng màu mà lớp phủ camera key ra — nên OBS cũng "
                  "key sân khấu được."),
            ],
            actions=[{"label": T("Green key & camera overlay", "Key xanh & lớp phủ camera"),
                      "href": "features/camera.html", "kind": "btn-ghost", "icon": "camera"}],
            media=framed(doc, "stage-gpu-storm",
                         T("Electric Storm on the GPU stage", "Electric Storm trên sân khấu GPU"),
                         T("What you see is what gets recorded: the same frame, drawn a second time off-screen at "
                           "the recording's own size and frame rate.",
                           "Những gì bạn thấy là những gì được ghi: cùng khung hình đó, vẽ thêm lần nữa ở chế độ "
                           "off-screen đúng kích thước và fps của bản ghi."),
                         badge=T("GPU stage · REC", "Sân khấu GPU · REC")),
        ),

        steps(
            id="take",
            cols=4,
            eyebrow=T("A take", "Một bản ghi"),
            title=T("From preset to published video", "Từ preset tới video đăng lên"),
            items=[
                {"t": T("Set the output", "Đặt đầu ra"),
                 "d": T("Recording → OUTPUT: format, resolution (window / 720p / 1080p), frame rate 15–60, Record "
                        "audio, and Transparent background for PNG.",
                        "Recording → OUTPUT: định dạng, độ phân giải (cửa sổ / 720p / 1080p), tốc độ khung 15–60, "
                        "Record audio, và Transparent background cho PNG.")},
                {"t": T("Choose the look", "Chọn diện mạo"),
                 "d": T("Pick a preset in Style, an interface in Theme, and load the score you want to play.",
                        "Chọn preset ở trang Style, giao diện ở trang Theme, và nạp bản nhạc bạn muốn chơi.")},
                {"t": T("Press REC", "Bấm REC"),
                 "d": T("REC sits in the corner of the stage: press it, choose where the take goes, play, then press "
                        "it again to stop.",
                        "Nút REC nằm ở góc sân khấu: bấm, chọn nơi lưu, chơi, rồi bấm lại để dừng.")},
                {"t": T("Take the file", "Lấy tệp"),
                 "d": T("The dialog reports the length and, for AVI or PNG, prints the ffmpeg line that finishes the "
                        "job.",
                        "Hộp thoại báo độ dài và, với AVI hoặc PNG, in sẵn dòng lệnh ffmpeg để hoàn tất.")},
            ],
        ),

        codeblock(
            id="ffmpeg",
            eyebrow=T("After the take", "Sau khi ghi"),
            title=T("Two ffmpeg lines you will actually use", "Hai dòng lệnh ffmpeg bạn thật sự sẽ dùng"),
            label=E("PowerShell"),
            text=('<span class="c"># AVI + WAV  ->  one MP4 (video copied, audio encoded)</span>\n'
                  'ffmpeg -i video.avi -i take.wav -c:v copy -c:a aac take.mp4\n\n'
                  '<span class="c"># PNG sequence with alpha  ->  WebM with alpha</span>\n'
                  'ffmpeg -framerate 60 -i frame-%06d.png -c:v libvpx-vp9 -pix_fmt yuva420p take.webm'),
            note=T("sequence.json, written next to the frames, carries the size, the frame rate, the frame count and "
                   "a suggested command for exactly this.",
                   "Tệp sequence.json nằm cạnh các khung hình đã ghi sẵn kích thước, tốc độ khung hình, số khung và "
                   "một dòng lệnh gợi ý cho đúng việc này."),
        ),

        callout(
            style="warn",
            icon="alert",
            title=T("What recording cannot do yet", "Ghi hình chưa làm được gì"),
            body=[T("There is no direct WebM/VP9 writer — the 32-bit PNG sequence is the path to alpha video, and "
                    "sequence.json suggests the ffmpeg line that builds it. MP4 needs Windows' own encoders, so a "
                    "machine without H.264 cannot write that format at all, and a machine without AAC records the "
                    "picture only.",
                    "Chưa ghi trực tiếp được WebM/VP9 — chuỗi PNG 32-bit là đường dẫn tới video alpha, và "
                    "sequence.json gợi ý dòng lệnh ffmpeg để dựng nó. MP4 cần bộ mã hoá của chính Windows, nên máy "
                    "không có H.264 thì không ghi được định dạng này, còn máy thiếu AAC thì bản ghi chỉ có hình.")],
        ),

        pagenav(prev=("features/sound.html", "sound"), next=("features/design.html", "design")),
        cta(
            title=T("Your next video is one key away", "Video tiếp theo của bạn chỉ cách một phím"),
            sub=T("REC is on the stage from the first launch — MP4 with the sound already inside it.",
                  "Nút REC có ngay trên sân khấu từ lần mở đầu — MP4 đã có sẵn tiếng bên trong."),
            actions=[DOWNLOAD,
                     {"label": T("Looks, presets & themes", "Diện mạo, preset & theme"),
                      "href": "features/design.html", "kind": "btn-ghost", "icon": "arrow"}],
        ),
    ]
    return {
        "title": T("Recording & export: MP4, AVI, PNG with alpha · Keyflow",
                   "Ghi hình & xuất bản: MP4, AVI, PNG trong suốt · Keyflow"),
        "description": T(
            "Record the Keyflow stage to MP4 with H.264 video and AAC audio in one file, to AVI with a WAV beside "
            "it, or to a 32-bit PNG sequence with transparency — at window, 720p or 1080p and 15–60 fps, drawn "
            "off-screen at the recording's own size.",
            "Ghi sân khấu Keyflow ra MP4 gồm video H.264 và âm thanh AAC trong một tệp, ra AVI kèm tệp WAV bên "
            "cạnh, hoặc ra chuỗi PNG 32-bit trong suốt — ở mức theo cửa sổ, 720p hoặc 1080p và 15–60 fps, được vẽ "
            "off-screen đúng kích thước của bản ghi."),
        "og_image": "previews/en/recording-dock.png",
        "crumb_trail": TRAIL + [("Recording & export", "features/recording.html")],
        "body": body,
    }


# ===========================================================================
# 5. Looks, presets & themes
# ===========================================================================
PRESETS = [
    ("Concert Gold", T("The default: champagne gold on ebony, matched to the Concert Grand interface.",
                       "Mặc định: vàng champagne trên nền gỗ đen, hợp với giao diện Concert Grand.")),
    ("Neon Violet", T("A dark hall, violet neon and clean trails.",
                      "Hội trường tối, neon tím và vệt sáng gọn.")),
    ("Inferno", T("Fire notes with an animated burning texture and warm sparks.",
                  "Nốt lửa có vân cháy chuyển động và tia lửa ấm.")),
    ("Aurora Rainbow", T("Rainbow colour by pitch over an aurora backdrop.",
                         "Màu cầu vồng theo cao độ trên nền cực quang.")),
    ("Ice Crystal", T("Cold glass notes, pale bloom and a still stage.",
                      "Nốt thuỷ tinh lạnh, bloom nhạt và sân khấu tĩnh.")),
    ("Two Hands", T("Per-hand colours with a split point you can move.",
                    "Màu theo từng tay với điểm chia đổi được.")),
    ("Classic Roll", T("A quiet, readable piano roll with almost no effects.",
                       "Piano roll gọn, dễ đọc, gần như không hiệu ứng.")),
    ("Green Screen", T("A pure green backdrop for keying in OBS or an editor.",
                       "Nền xanh lá thuần để key trong OBS hoặc phần mềm dựng.")),
    ("Sakura Nocturne", T("Petals drifting through a night stage.",
                          "Cánh hoa anh đào trôi trong sân khấu đêm.")),
    ("Moonlight Sonata", T("A restrained, moonlit look for slow movements.",
                           "Diện mạo dưới trăng, tiết chế, hợp với chương chậm.")),
    ("Galaxy Voyage", T("Rainbow trails over a cosmic ambient layer.",
                        "Vệt cầu vồng trên lớp nền vũ trụ.")),
    ("Electric Storm", T("Speed lines and electric arcs between the keys you hold.",
                         "Vệt tốc độ và tia điện nối các phím đang giữ.")),
    ("Ocean Depths", T("Deep water colours with the Ocean Flow shader background.",
                       "Màu nước sâu cùng nền shader Ocean Flow.")),
    ("Retro Arcade", T("A retro grid backdrop and bright, flat colours.",
                       "Nền lưới retro và màu phẳng rực rỡ.")),
]


def build_design(doc) -> dict:
    body = [
        feature_hero(
            doc,
            crumb=T("Looks, presets & themes", "Diện mạo, preset & theme"),
            eyebrow=T("Stage design studio", "Xưởng thiết kế sân khấu"),
            title=T("A whole look, in one line of text", "Cả một diện mạo, trong một dòng chữ"),
            lead=T("Fourteen presets, three concert interfaces, a theme studio that derives twenty colours from five, "
                   "a design dock of thirteen pages with a search box that answers in both languages — and a share "
                   "code that carries your entire look to another machine.",
                   "Mười bốn preset, ba giao diện hoà nhạc, một xưởng theme suy ra hai mươi màu từ năm màu gốc, "
                   "bàn thiết kế mười ba trang với ô tìm kiếm trả lời bằng cả hai ngôn ngữ — và một mã chia sẻ mang "
                   "toàn bộ diện mạo của bạn sang máy khác."),
            chips=[
                T("14 presets + 3 community", "14 preset + 3 cộng đồng"),
                T("3 concert interfaces", "3 giao diện hoà nhạc"),
                T("13 dock pages in 4 groups", "13 trang dock trong 4 nhóm"),
                T("32 undo states", "32 trạng thái hoàn tác"),
                E("KEYFLOW-LOOK-2:…"),
            ],
            shot="theme-dock",
            alt=T("The Theme page: three concert interfaces and the theme studio",
                  "Trang Theme: ba giao diện hoà nhạc và xưởng theme"),
            cap=T("Theme: the three concert interfaces, motion level, backdrop density, the user theme studio and "
                  "the quick looks.",
                  "Theme: ba giao diện hoà nhạc, mức chuyển động, mật độ backdrop, xưởng theme người dùng và các "
                  "nút look nhanh."),
            badge=T("Stage design · Theme", "Thiết kế sân khấu · Theme"),
        ),

        band(stats=[
            (("13", "13"), T("pages in the design dock", "trang trong bàn thiết kế"), 13),
            (("4", "4"), T("groups they are arranged in", "nhóm sắp xếp các trang đó"), 4),
            (("14 + 3", "14 + 3"), T("presets, built-in and community", "preset dựng sẵn và cộng đồng"), None),
            (("5 → 20", "5 → 20"), T("colours you pick, tokens derived", "màu bạn chọn, token được suy ra"), None),
        ]),

        split(
            id="dock",
            eyebrow=T("The dock", "Bàn thiết kế"),
            title=T("Thirteen pages, one search box, everything saves itself",
                    "Mười ba trang, một ô tìm kiếm, mọi thứ tự lưu"),
            ticks=[
                T("Search matches the English label and the translated one, plus synonyms and setting ids: “speed”, "
                  "“tốc độ”, “fps”, “tempo” and NoteFallSpeed all land on the same Fall speed slider, with the match "
                  "highlighted in the accent colour and the first page that has results opened for you.",
                  "Ô tìm kiếm khớp cả nhãn tiếng Anh lẫn bản dịch, cùng từ đồng nghĩa và id cài đặt: “speed”, "
                  "“tốc độ”, “fps”, “tempo” và NoteFallSpeed đều ra cùng thanh trượt Fall speed, phần khớp được tô "
                  "màu accent và trang đầu tiên có kết quả tự mở ra."),
                T("Every parameter has a slider, a numeric box that accepts units, comma decimals and note names "
                  "like C4, and its own reset button; rows that depend on a switch hide and show themselves.",
                  "Mỗi thông số có một thanh trượt, một ô nhập số chấp nhận đơn vị, dấu phẩy thập phân và tên nốt "
                  "như C4, cùng nút reset riêng; các hàng phụ thuộc một công tắc thì tự ẩn/hiện."),
                T("SAVE and RESET PAGE sit on every page, and changes save themselves after 0.65 s.",
                  "Mỗi trang đều có SAVE và RESET PAGE, và thay đổi tự lưu sau 0,65 giây."),
                T("Tab keeps focus inside the dock and walks the pages in the order their rows are printed; at "
                  "1080×700 every row still fits the scrolling column.",
                  "Tab giữ tiêu điểm trong dock và đi qua từng trang theo đúng thứ tự các hàng được in; ở cỡ cửa sổ "
                  "1080×700 mọi hàng vẫn nằm trong cột cuộn."),
            ],
            actions=[{"label": T("Keyboard shortcuts", "Bàn phím & phím tắt"),
                      "href": "guide.html#shortcuts", "kind": "btn-ghost", "icon": "keys"}],
            media=framed(doc, "design-dock",
                         T("The Style page of the design dock", "Trang Style của bàn thiết kế"),
                         T("Style: built-in, community and user presets, the quick layer switches, the GO TO card "
                           "and the share code buttons.",
                           "Style: preset dựng sẵn, cộng đồng và của người dùng, các công tắc bật nhanh từng lớp, "
                           "thẻ GO TO và hai nút mã chia sẻ."),
                         badge=T("Stage design · Style", "Thiết kế sân khấu · Style")),
        ),

        groups(
            id="pages",
            eyebrow=T("Interface map", "Bản đồ giao diện"),
            title=T("Four groups, thirteen pages — the layout the code, the XAML and the tests all read",
                    "Bốn nhóm, mười ba trang — bố cục mà cả mã nguồn, XAML và bộ kiểm thử cùng đọc"),
            groups=[
                {"name": T("Stage design", "Thiết kế sân khấu"), "icon": "palette", "items": [
                    (E("Style"), T("Presets, thirteen quick layer switches, the GO TO card and the share code.",
                                   "Preset, mười ba công tắc bật nhanh từng lớp, thẻ GO TO và mã chia sẻ.")),
                    (E("Theme"), T("Three concert interfaces, motion level, backdrop density and the theme studio.",
                                   "Ba giao diện hoà nhạc, mức chuyển động, mật độ backdrop và xưởng theme.")),
                    (E("Notes"), T("Colour, shape, glow, fall direction and speed, hold effects, smart modulators.",
                                   "Màu, hình dáng, glow, hướng và tốc độ rơi, hiệu ứng giữ, bộ điều biến.")),
                    (E("Particles"), T("Spark emitter and physics, plasma wisps, fire, rings, impact waves and "
                                       "flashes, trails, ghosts, release effects.",
                                       "Emitter tia lửa và physics, wisp plasma, lửa, vòng sóng, sóng và chớp va "
                                       "chạm, vệt rơi, bóng ma, hiệu ứng nhả.")),
                    (E("Keyboard"), T("Key style, labels, red felt, lighting and the ray-traced shading group.",
                                      "Kiểu phím, nhãn phím, nỉ đỏ, chiếu sáng và nhóm đổ bóng ray-tracing.")),
                    (E("Background"), T("Colour, picture or green screen, atmosphere, guide lanes, halo and the four "
                                        "ambient layers.",
                                        "Màu, ảnh hoặc green screen, bầu khí quyển, guide lanes, halo và bốn lớp "
                                        "ambient.")),
                    (E("Camera & FX"), T("Parallax, zoom, frame, saturation, contrast, bloom, the camera overlay and "
                                         "hand tracking.",
                                         "Parallax, zoom, khung hình, bão hoà, tương phản, bloom, lớp phủ camera và "
                                         "theo dõi bàn tay.")),
                ]},
                {"name": T("Sound & input", "Âm thanh & đầu vào"), "icon": "wave", "items": [
                    (E("Audio"), T("Download and load the one Salamander piano, pick the reverb and its room, string "
                                   "resonance, gain and the output backend.",
                                   "Tải và nạp cây Salamander duy nhất, chọn reverb và căn phòng, cộng hưởng "
                                   "dây, gain và backend đầu ra.")),
                    (E("MIDI"), T("Input and output devices, the track list with solo/mute/colour, and the "
                                  "metronome.",
                                  "Thiết bị vào và ra, danh sách track có solo/mute/màu, và metronome.")),
                ]},
                {"name": T("Session", "Phiên làm việc"), "icon": "target", "items": [
                    (E("Practice"), T("Practice modes, tempo, the A-B loop and the automatic practice tempo.",
                                      "Chế độ tập, tempo, vòng lặp A-B và tempo luyện tập tự động.")),
                    (E("History"), T("Every run of the open song, the fourteen-day chart, the ghost, HTML export.",
                                     "Từng lượt chơi của bài đang mở, biểu đồ 14 ngày, bóng luyện tập, xuất HTML.")),
                    (E("Recording"), T("The OUTPUT card: format, resolution, frame rate, audio and transparency.",
                                       "Thẻ OUTPUT: định dạng, độ phân giải, tốc độ khung hình, tiếng và nền "
                                       "trong suốt.")),
                ]},
                {"name": E("App"), "icon": "chip", "items": [
                    (E("General"), T("Interface language, the graphics engine — GPU frame rate, VSync, the GPU stage "
                                     "window, the engine status line — and the settings profile.",
                                     "Ngôn ngữ giao diện, engine đồ hoạ — tốc độ khung GPU, VSync, cửa sổ sân khấu "
                                     "GPU, dòng trạng thái engine — và hồ sơ cài đặt.")),
                ]},
            ],
        ),

        table(
            id="presets",
            eyebrow=T("Presets", "Preset"),
            title=T("Fourteen looks, each with the interface that suits it",
                    "Mười bốn diện mạo, mỗi preset kèm giao diện hợp với nó"),
            head=[E("Preset"), T("Character", "Tính cách")],
            rows=[[E(name), desc] for name, desc in PRESETS],
            note=T("Three community presets ship inside the build as well, labelled COMMUNITY: they apply like any "
                   "other preset but cannot be deleted or overwritten. Presets whose theme is meant to move — Galaxy "
                   "Voyage, Electric Storm, Aurora Rainbow — pick the motion that fits; Classic Roll, Lo-Fi and "
                   "Green Screen keep the stage still or plain when that suits the piece.",
                   "Ngoài ra còn ba preset cộng đồng được nhúng trong bản dựng, dán nhãn COMMUNITY: áp dụng như mọi "
                   "preset khác nhưng không xoá và không ghi đè được. Những preset có chủ đề chuyển động — Galaxy "
                   "Voyage, Electric Storm, Aurora Rainbow — sẽ chọn kiểu chuyển động hợp chủ đề; Classic Roll, "
                   "Lo-Fi và Green Screen giữ sân khấu tĩnh hoặc gọn khi bản nhạc cần như vậy."),
        ),

        split(
            id="user-presets",
            flip=True,
            eyebrow=T("Your own presets", "Preset của riêng bạn"),
            title=T("Saved with a real thumbnail of your own stage",
                    "Lưu kèm ảnh thu nhỏ render từ chính sân khấu của bạn"),
            ticks=[
                T("SAVE AS writes a small JSON file into the presets folder of your settings directory, together with "
                  "a 192×112 picture rendered by the stage itself — so an exported preset shows its actual look on "
                  "somebody else's machine.",
                  "SAVE AS ghi một tệp JSON nhỏ vào thư mục presets của thư mục cài đặt, kèm ảnh 192×112 do chính "
                  "sân khấu render — nên preset đem xuất sẽ hiện đúng diện mạo thật trên máy người khác."),
                T("Older presets without a picture get a miniature drawn from their settings instead, so the list "
                  "never shows an empty box.",
                  "Preset cũ không có ảnh thì danh sách tự vẽ một miniature từ cài đặt của nó, nên không bao giờ "
                  "hiện ô trống."),
                T("DELETE, IMPORT and EXPORT are on the same page, and the header shows the preset name with a * as "
                  "soon as you have changed something.",
                  "DELETE, IMPORT và EXPORT nằm cùng trang, và header hiện tên preset kèm dấu * ngay khi bạn đã "
                  "chỉnh gì đó."),
                T("Copying the presets folder carries them to another machine — or use IMPORT/EXPORT for one at a "
                  "time. A corrupt file is skipped instead of breaking the list.",
                  "Chép thư mục presets là mang chúng sang máy khác — hoặc dùng IMPORT/EXPORT cho từng cái một. "
                  "Tệp hỏng bị bỏ qua chứ không làm hỏng cả danh sách."),
            ],
            media=framed(doc, "main-menu",
                         T("The start menu with the interface language chips",
                           "Menu khởi động với chip chọn ngôn ngữ giao diện"),
                         T("The start menu: Perform & Play, Quick Adjustments for the most-used controls, Piano & Audio "
                           "Setup and MIDI Devices straight into their pages, the language chips — and Stage "
                           "Design Studio for the full dock.",
                           "Menu khởi động: Perform & Play, Quick Adjustments cho các điều khiển hay dùng, Piano & "
                           "Audio Setup và MIDI Devices mở thẳng vào trang tương ứng, chip chọn ngôn ngữ — và "
                           "Stage Design Studio cho bàn thiết kế đầy đủ."),
                         badge=T("Start menu", "Menu khởi động")),
        ),

        split(
            id="share",
            eyebrow=T("Share codes", "Mã chia sẻ"),
            title=T("COPY CODE, paste it in a chat, APPLY CODE",
                    "COPY CODE, dán vào khung chat, rồi APPLY CODE"),
            ticks=[
                T("A code is the whole look — every visual setting, and since version 2 the note width-by-velocity "
                  "and fade graphs the AR overlay draws from too — gzipped into base64url behind a "
                  "KEYFLOW-LOOK-2: version prefix, so one line of text carries it.",
                  "Một mã chia sẻ là toàn bộ diện mạo — mọi cài đặt hình ảnh, và từ phiên bản 2 còn có cả đồ thị "
                  "độ rộng và độ mờ theo velocity mà lớp phủ AR dùng — nén gzip rồi mã hoá base64url sau tiền tố "
                  "phiên bản KEYFLOW-LOOK-2:, nên chỉ một dòng chữ là mang đi được."),
                T("It round-trips every value but deliberately drops the sender's background image path: a look that "
                  "used a picture falls back to a solid colour rather than pointing at a file you do not have.",
                  "Mã đi-về đúng từng giá trị nhưng cố ý bỏ đường dẫn ảnh nền của máy người gửi: diện mạo dùng ảnh "
                  "sẽ rơi về nền màu thay vì trỏ tới một tệp bạn không có."),
                T("Codes made by version 1 (KEYFLOW-LOOK-1:…) still open bit for bit — the envelope was complete from "
                  "day one — and a code that a chat window wrapped over several lines still reads.",
                  "Mã do phiên bản 1 tạo (KEYFLOW-LOOK-1:…) vẫn mở được đúng từng bit — phần vỏ đã đầy đủ ngay "
                  "từ đầu — và mã bị cửa sổ chat xuống dòng vẫn đọc được."),
                T("An empty, unknown, other-version, oversized or corrupt code is rejected with the reason printed "
                  "right in the dock — and your current settings are left alone.",
                  "Mã rỗng, lạ, khác phiên bản, quá lớn hoặc hỏng bị từ chối kèm lý do in ngay trong dock — và cài "
                  "đặt hiện tại của bạn được giữ nguyên."),
            ],
            media=_codecard(
                doc, "share",
                T("What a shared look looks like", "Một diện mạo được chia sẻ trông ra sao"),
                "KEYFLOW-LOOK-2:H4sIAAAAAAAACqvWKkktLlGy\n"
                "UlAqS8wpTtVRSs7PS8nMS1eqBQBJFvYhHAAAAA==",
                T("A real code is longer; the shape is what matters — one prefix, one blob of text, and it pastes "
                  "anywhere.",
                  "Mã thật dài hơn; điều quan trọng là hình dạng của nó — một tiền tố, một khối chữ, và dán được ở "
                  "bất kỳ đâu."),
            ),
        ),

        split(
            id="themes",
            flip=True,
            eyebrow=T("Concert interfaces", "Giao diện hoà nhạc"),
            title=T("Three interfaces, swapped in a single frame", "Ba giao diện, đổi trong một khung hình"),
            ticks=[
                T("Concert Grand — Steinway ebony and champagne gold — is the default; Concert Noir is obsidian and "
                  "platinum; Velvet Gold is mahogany velvet and brass.",
                  "Concert Grand — gỗ đen Steinway và vàng champagne — là mặc định; Concert Noir là obsidian và "
                  "platinum; Velvet Gold là nhung đỏ mahogany và đồng thau."),
                T("Changing the theme swaps every surface and accent through DynamicResource in the current frame — "
                  "no restart, no half-themed window — and each theme brings its own animated backdrop: resonance "
                  "waves, aurora, velvet.",
                  "Đổi theme là đổi toàn bộ surface và accent qua DynamicResource ngay trong khung hình hiện tại — "
                  "không khởi động lại, không cửa sổ nửa vời — và mỗi theme kèm backdrop động riêng: sóng cộng "
                  "hưởng, quầng cực quang, nhung."),
                T("The same page holds the motion level and the backdrop density, and a QUICK LOOKS card with three "
                  "one-click buttons: Concert Grand, Concert Gold and Moonlight.",
                  "Cùng trang đó có mức chuyển động và mật độ backdrop, kèm thẻ QUICK LOOKS với ba nút một chạm: "
                  "Concert Grand, Concert Gold và Moonlight."),
            ],
            media=framed(doc, "theme-dock",
                         T("The Theme page of the design dock", "Trang Theme của bàn thiết kế"),
                         T("Theme: the three concert interfaces, the user theme studio and the quick looks.",
                           "Theme: ba giao diện hoà nhạc, xưởng theme người dùng và các nút look nhanh."),
                         badge=T("Stage design · Theme", "Thiết kế sân khấu · Theme")),
        ),

        split(
            id="studio",
            eyebrow=T("The theme studio", "Xưởng theme"),
            title=T("Pick five colours; twenty more are derived so text stays readable",
                    "Chọn năm màu; hai mươi màu còn lại được suy ra để chữ luôn đọc được"),
            ticks=[
                T("Theme → USER THEMES → CREATE / EDIT / DELETE opens the studio: a name, a backdrop family "
                  "(Acoustic, Obsidian or Imperial) and five colours — accent, secondary accent, glow, surface and "
                  "bright particles.",
                  "Theme → USER THEMES → CREATE / EDIT / DELETE mở xưởng theme: một cái tên, một họ nền động "
                  "(Acoustic, Obsidian hoặc Imperial) và năm màu — màu nhấn, màu nhấn phụ, màu phát sáng, màu bề "
                  "mặt và màu hạt sáng."),
                T("The other twenty interface tokens are derived from those five, which is why you cannot build a "
                  "palette with unreadable text; a preview strip updates as you type.",
                  "Hai mươi token giao diện còn lại được suy ra từ năm màu đó, nên bạn không thể tạo ra một bảng "
                  "màu khiến chữ không đọc được; dải xem trước cập nhật ngay khi bạn gõ."),
                T("Themes are saved as small JSON files in the themes folder of your settings directory — hand "
                  "editable, healed if you make a mistake, ignored if they are corrupt, and listed beside the three "
                  "built-ins in both chip rows.",
                  "Theme được lưu thành tệp JSON nhỏ trong thư mục themes của thư mục cài đặt — sửa tay được, tự "
                  "chữa khi bạn sửa sai, bị bỏ qua khi hỏng, và hiện cạnh ba theme có sẵn ở cả hai hàng chip."),
                T("The studio refuses to save without a name or with a colour that is not hex, and a theme's id "
                  "stays stable because it comes from its name.",
                  "Xưởng từ chối lưu khi thiếu tên hoặc màu không phải dạng hex, và id của theme ổn định vì được "
                  "lấy từ chính cái tên."),
            ],
            media=framed(doc, "design-dock",
                         T("The design dock where themes and presets are chosen",
                           "Bàn thiết kế nơi chọn theme và preset"),
                         T("Every visual decision lives in the same dock — and one search box covers all thirteen "
                           "pages.",
                           "Mọi quyết định hình ảnh đều nằm trong cùng một bàn thiết kế — và một ô tìm kiếm bao "
                           "trùm cả mười ba trang."),
                         badge=T("Stage design", "Thiết kế sân khấu")),
        ),

        split(
            id="profiles",
            flip=True,
            eyebrow=T("Undo & profiles", "Hoàn tác & hồ sơ"),
            title=T("Thirty-two ways back, and one file that carries everything",
                    "Ba mươi hai bước lùi, và một tệp mang theo tất cả"),
            ticks=[
                T("Ctrl+Z steps back and Ctrl+Shift+Z (or Ctrl+Y) steps forward through the last 32 states of the "
                  "dock; one slider drag — or one burst of tweaks — counts as a single step, and Ctrl+Z never steals "
                  "the undo of the box you are typing in.",
                  "Ctrl+Z lùi và Ctrl+Shift+Z (hoặc Ctrl+Y) tiến qua 32 trạng thái gần nhất của bàn thiết kế; một "
                  "lần kéo slider — hoặc một đợt chỉnh liên tiếp — tính là một bước, và Ctrl+Z không giành quyền "
                  "hoàn tác của ô bạn đang gõ."),
                T("A snapshot is the JSON of the visual settings, so undo goes through exactly the same clamping as "
                  "setting a value yourself; changing preset is a mark too, and importing a profile starts a new "
                  "history you cannot undo past.",
                  "Ảnh chụp là JSON của cài đặt hình ảnh, nên hoàn tác đi qua đúng bước kẹp giá trị như khi bạn tự "
                  "đặt; đổi preset cũng là một mốc, còn nhập hồ sơ thì mở một lịch sử mới không lùi qua được."),
                T("IMPORT/EXPORT PROFILE… on the General page packs stage settings, language and interface into one "
                  "Keyflow.profile.json — drag it onto the window to apply it.",
                  "IMPORT/EXPORT PROFILE… ở trang General gói cài đặt sân khấu, ngôn ngữ và giao diện vào một tệp "
                  "Keyflow.profile.json — kéo thả tệp vào cửa sổ là áp dụng."),
                T("Drop a .mid or .midi file on the window to open it, or drop a picture to set it as the stage "
                  "background. A language missing from the build falls back to English rather than leaving a "
                  "half-translated interface.",
                  "Thả tệp .mid hoặc .midi vào cửa sổ để mở bài, thả một bức ảnh để đặt làm nền sân khấu. Ngôn ngữ "
                  "không có trong bản dựng sẽ rơi về tiếng Anh chứ không để giao diện nửa dịch."),
            ],
            media=framed(doc, "language-dock",
                         T("The General page: language, graphics engine and settings profile",
                           "Trang General: ngôn ngữ, engine đồ hoạ và hồ sơ cài đặt"),
                         T("General: interface language, the graphics engine card and the settings profile card.",
                           "General: ngôn ngữ giao diện, thẻ engine đồ hoạ và thẻ hồ sơ cài đặt."),
                         badge=T("App · General", "Ứng dụng · General")),
        ),

        specdl(
            id="files",
            eyebrow=T("On disk", "Trên đĩa"),
            title=T("Where your looks live", "Diện mạo của bạn nằm ở đâu"),
            items=[
                (E("%LOCALAPPDATA%\\Keyflow\\visual-settings.json"),
                 T("The current settings. Delete this file — or press RESET TO DEFAULT in the dock — to start over.",
                   "Cài đặt hiện tại. Xoá tệp này — hoặc bấm RESET TO DEFAULT trong dock — để làm lại từ đầu.")),
                (E("%LOCALAPPDATA%\\Keyflow\\presets\\*.json"),
                 T("Your presets, each with its rendered thumbnail. Copy the folder to carry them to another machine.",
                   "Preset của bạn, mỗi tệp kèm ảnh thu nhỏ đã render. Chép cả thư mục để mang sang máy khác.")),
                (E("%LOCALAPPDATA%\\Keyflow\\themes\\*.json"),
                 T("The themes you made, as small hand-editable files.",
                   "Những theme bạn tự tạo, dưới dạng tệp nhỏ sửa tay được.")),
                (E("%LOCALAPPDATA%\\Keyflow\\library.json"),
                 T("Recent songs and the values each one was played at.",
                   "Bài mở gần đây và các giá trị đã dùng cho từng bài.")),
                (E("%LOCALAPPDATA%\\Keyflow\\history\\practice.jsonl"),
                 T("One line per practice run, newest first.",
                   "Mỗi lượt luyện tập một dòng, mới nhất trước.")),
                (E("--settings-dir=&lt;folder&gt;"),
                 T("Move all of it somewhere else — useful for a portable setup or a second profile.",
                   "Dời tất cả sang nơi khác — hữu ích cho bản chạy di động hoặc một hồ sơ thứ hai.")),
            ],
        ),

        callout(
            style="tip",
            icon="shield",
            title=T("Accessible by design, and checked", "Trợ năng có chủ đích, và được kiểm tra"),
            body=[T("Every glyph-only button — the A, B and × loop buttons, the reset arrows, the window buttons, the "
                    "Play dialog chevrons — has a screen-reader name taken from its own translated tooltip, so it "
                    "follows the language. Auto-generated dock rows are named after their labels, Tab cycles inside "
                    "the dock, and when Windows switches to high contrast the chrome is painted with the system "
                    "colours while your chosen theme stays saved.",
                    "Mọi nút chỉ có glyph — nút vòng lặp A, B và ×, các mũi tên reset, nút cửa sổ, chevron của hộp "
                    "thoại Play — đều có tên cho trình đọc màn hình lấy từ chính tooltip đã dịch, nên đổi ngôn ngữ "
                    "là đổi theo. Các hàng sinh tự động trong dock được đặt tên theo nhãn của hàng, Tab xoay vòng "
                    "trong dock, và khi Windows bật high contrast thì khung giao diện vẽ bằng màu hệ thống trong khi "
                    "theme bạn chọn vẫn được giữ nguyên trong tệp cài đặt.")],
        ),

        pagenav(prev=("features/recording.html", "recording"), next=("features/camera.html", "camera")),
        cta(
            title=T("Make it look like yours", "Làm cho nó trông như của bạn"),
            sub=T("Pick a preset, or build a theme from five colours and share the whole look in one line.",
                  "Chọn một preset, hoặc dựng một theme từ năm màu rồi chia sẻ cả diện mạo bằng một dòng chữ."),
            actions=[DOWNLOAD,
                     {"label": T("Camera & hand tracking", "Camera & theo dõi bàn tay"),
                      "href": "features/camera.html", "kind": "btn-ghost", "icon": "arrow"}],
        ),
    ]
    return {
        "title": T("Presets, themes & the design dock · Keyflow",
                   "Preset, theme & bàn thiết kế · Keyflow"),
        "description": T(
            "Fourteen built-in presets and three community looks, three concert interfaces, a theme studio that "
            "derives twenty colours from five, a thirteen-page design dock with bilingual search, 32 undo states, "
            "settings profiles and one-line share codes.",
            "Mười bốn preset dựng sẵn cùng ba look cộng đồng, ba giao diện hoà nhạc, xưởng theme suy ra hai mươi màu "
            "từ năm màu, bàn thiết kế mười ba trang có tìm kiếm song ngữ, 32 trạng thái hoàn tác, hồ sơ cài đặt và "
            "mã chia sẻ một dòng."),
        "og_image": "previews/en/theme-dock.png",
        "crumb_trail": TRAIL + [("Looks, presets & themes", "features/design.html")],
        "body": body,
    }


# ===========================================================================
# 6. Camera & hand tracking
# ===========================================================================
def build_camera(doc) -> dict:
    body = [
        feature_hero(
            doc,
            crumb=T("Camera & hand tracking", "Camera & theo dõi bàn tay"),
            eyebrow=E("Camera & FX"),
            title=T("Put yourself on the stage — and the stage over your own piano",
                    "Đưa bạn lên sân khấu — và đưa sân khấu lên chính cây đàn của bạn"),
            lead=T("Draw a live webcam or a looping video file onto the stage in any corner, key out a green "
                   "backdrop, and turn on hand tracking: Keyflow reads your hands straight out of the camera frame "
                   "with classical computer vision — no model, no download, nothing leaves your machine. The AR "
                   "overlay goes further and draws the falling notes over your real keyboard, calibrated from four "
                   "marked corners.",
                   "Vẽ một webcam trực tiếp hoặc một tệp video chạy lặp lên sân khấu ở bất kỳ góc nào, key nền "
                   "xanh, và bật theo dõi bàn tay: Keyflow đọc bàn tay ngay từ khung camera bằng thị giác máy tính "
                   "cổ điển — không mô hình, không tải gì thêm, không gì rời khỏi máy bạn. Lớp phủ AR còn đi xa "
                   "hơn: vẽ nốt rơi đè lên chính cây đàn thật, hiệu chỉnh từ bốn góc được đánh dấu."),
            chips=[
                T("Live camera or video file", "Camera trực tiếp hoặc tệp video"),
                T("4 corners · up to 60 fps", "4 góc · tới 60 fps"),
                T("Green key, 0–100 tolerance", "Key xanh, dung sai 0–100"),
                T("AR overlay on the real keys", "Lớp phủ AR trên phím thật"),
                T("Hand tracking, no ML model", "Theo dõi tay, không mô hình ML"),
            ],
            shot="stage-live",
            alt=T("The live stage where the camera overlay is drawn",
                  "Sân khấu live nơi lớp phủ camera được vẽ"),
            cap=T("The live stage: the camera overlay is composited into a corner of this same frame, the hand "
                  "marker sits on the keys themselves, and the AR overlay puts this whole picture over your own "
                  "keyboard.",
                  "Sân khấu live: lớp phủ camera được ghép vào một góc của chính khung hình này, điểm đánh dấu "
                  "bàn tay nằm ngay trên phím, còn lớp phủ AR đặt cả khung hình này lên cây đàn thật của bạn."),
            badge=E("Camera & FX"),
        ),

        band(stats=[
            (("60", "60"), T("fps the camera can reach the stage at", "fps camera có thể lên sân khấu"), 60),
            (("4", "4"), T("corners to mark for the AR calibration", "góc cần đánh dấu cho hiệu chỉnh AR"), 4),
            (("0–300 ms", "0–300 ms"), T("camera delay, remembered per camera",
                                         "độ trễ camera, nhớ theo từng camera"), None),
            (("0", "0"), T("models to download", "mô hình phải tải về"), 0),
        ]),

        split(
            id="overlay",
            eyebrow=T("Webcam overlay", "Lớp phủ webcam"),
            title=T("A camera window on the stage, keyed if you want it",
                    "Một cửa sổ camera trên sân khấu, key nền nếu bạn muốn"),
            ticks=[
                T("Camera overlay draws a live camera or a looping video file onto the stage as a small window. "
                  "The list is the machine's own: one line per camera with its real name (never “Camera 1”), kind, "
                  "port and VID/PID — and Automatic prefers colour cameras, ranks virtual ones after them and "
                  "infrared (Windows Hello) cameras last.",
                  "Camera overlay vẽ một camera trực tiếp hoặc một tệp video chạy lặp lên sân khấu như một cửa sổ "
                  "nhỏ. Danh sách là của chính máy bạn: mỗi camera một dòng với tên thật (không bao giờ là "
                  "“Camera 1”), loại, cổng và VID/PID — và chế độ Automatic ưu tiên camera màu, xếp camera ảo "
                  "sau đó và camera hồng ngoại (Windows Hello) cuối cùng."),
                T("Plugging a camera in or out, or starting and stopping OBS Virtual Camera, updates the list and "
                  "reopens the camera when it has to — but never while a take is being recorded, the delay is "
                  "being measured or the keys are being marked.",
                  "Cắm hoặc rút camera, hay bật/tắt OBS Virtual Camera, đều cập nhật danh sách và mở lại camera "
                  "khi cần — nhưng không bao giờ trong lúc đang ghi, đang đo độ trễ hay đang đánh dấu phím."),
                T("For a live camera the app picks the mode nearest 720p at the highest rate the camera offers — "
                  "up to 60 fps, MJPG preferred — reads at the camera's own pace instead of a fixed 30 fps cap, "
                  "shows the real mode in the status line (`720p · 60 fps · MJPG`) and passes frames through a "
                  "three-buffer ring so a slow draw cannot tear a picture.",
                  "Với camera trực tiếp, ứng dụng chọn mode gần 720p nhất ở tốc độ cao nhất camera có — tới 60 "
                  "fps, ưu tiên MJPG — đọc theo nhịp của camera thay vì khoá cứng 30 fps, hiện đúng mode thật ở "
                  "dòng trạng thái (`720p · 60 fps · MJPG`) và cho khung hình đi qua vòng ba buffer nên nhịp vẽ "
                  "chậm không làm rách hình."),
                T("Corner places it in any of the four corners, Size sets 15–60% of the stage width, Opacity and "
                  "Mirror do what they say, and Key tolerance goes from 0 (key off) to 100 (widest) to remove pure "
                  "green — exactly the colour of the Green Screen preset.",
                  "Corner đặt khung vào một trong bốn góc, Size chỉnh 15–60% chiều rộng sân khấu, Opacity và "
                  "Mirror đúng như tên gọi, còn Key tolerance chạy từ 0 (tắt key) tới 100 (rộng nhất) để loại bỏ "
                  "màu xanh lá thuần — đúng màu của preset Green Screen."),
                T("The status line under the rows says plainly which camera is open, which file is playing, or why "
                  "it cannot run: no camera on this machine, or no Media Foundation.",
                  "Dòng trạng thái dưới các hàng nói rõ đang mở camera nào, đang chạy tệp nào, hay vì sao không "
                  "chạy được: máy không có camera, hoặc máy không có Media Foundation."),
            ],
            media=framed(doc, "background-image",
                         T("A stage with a picture behind the keys, ready for an overlay",
                           "Sân khấu có ảnh nền sau bàn phím, sẵn sàng cho lớp phủ"),
                         T("The same stage that the overlay is composited onto — here with a picture background "
                           "instead of a shader one.",
                           "Chính sân khấu mà lớp phủ camera được ghép lên — ở đây dùng ảnh nền thay vì nền shader."),
                         badge=T("Background", "Nền sân khấu")),
        ),

        split(
            id="ar",
            flip=True,
            eyebrow=T("AR overlay", "Lớp phủ AR"),
            title=T("The notes fall onto your keyboard, not onto a piano roll",
                    "Nốt rơi xuống chính bàn phím của bạn, không phải một piano roll"),
            ticks=[
                T("The AR OVERLAY card turns the camera into a full-screen background and puts the stage on top of "
                  "it. Mark the four corners of your keyboard's key strip once, and the app solves the camera's "
                  "field of view and a full 3D pose for the keyboard from those marks.",
                  "Thẻ AR OVERLAY biến camera thành nền toàn màn hình và đặt sân khấu lên trên. Đánh dấu bốn góc "
                  "dải phím của cây đàn một lần, ứng dụng sẽ giải ra trường nhìn (FOV) của camera và pose 3D đầy "
                  "đủ cho bàn phím từ chính các điểm đó."),
                T("Calibrate has a Unity-style Move / Rotate / Scale gizmo plus numeric translation and uniform-"
                  "scale sliders, so a pose that is nearly right can be nudged instead of marked again. "
                  "Calibration version 5 stores the complete transform, the FOV and the baseline; versions 1–4 "
                  "still load — with zero translation and unit scale, v4 keeping its rotation, v3/v4 their saved "
                  "FOV.",
                  "Cửa sổ Calibrate có gizmo kiểu Unity Move / Rotate / Scale cùng thanh trượt số cho tịnh tiến và "
                  "scale đồng đều, nên pose gần đúng có thể chỉnh nhẹ thay vì đánh dấu lại. Calibration phiên bản "
                  "5 lưu đầy đủ transform, FOV và baseline; các phiên bản 1–4 vẫn nạp được — với translation 0 và "
                  "scale 1, riêng v4 giữ rotation, v3/v4 giữ FOV đã lưu."),
                T("Notes in perspective turns the falling notes into camera-facing quads drawn from that pose, and "
                  "their travel has its own aiming: a preview arrow is projected over the camera picture with "
                  "Screen-up and key-depth buttons plus independent Note direction tilt and azimuth controls — "
                  "none of which move the keyboard transform.",
                  "Notes in perspective biến nốt rơi thành các quad hướng về camera, vẽ từ chính pose đó, và hướng "
                  "bay của nốt có cách ngắm riêng: một mũi tên xem trước được chiếu lên ảnh camera, kèm hai nút "
                  "Screen-up và key-depth cùng hai thanh trượt Note direction tilt / azimuth độc lập — tất cả đều "
                  "không làm dịch chuyển transform của bàn phím."),
                T("Quality offers Lite, Standard and Ultra. Learn / Perform, look-ahead, opacity and key tint stay "
                  "available in AR exactly as they do on the flat stage.",
                  "Quality có Lite, Standard và Ultra. Learn / Perform, look-ahead, opacity và key tint vẫn dùng "
                  "được trong AR đúng như trên sân khấu phẳng."),
            ],
            media=framed(doc, "design-dock",
                         T("The dock page the AR OVERLAY card lives on",
                           "Trang dock chứa thẻ AR OVERLAY"),
                         T("The AR OVERLAY card sits on Camera & FX, right beside the webcam overlay and hand "
                           "tracking.",
                           "Thẻ AR OVERLAY nằm trên trang Camera & FX, ngay cạnh lớp phủ webcam và phần theo dõi "
                           "bàn tay."),
                         badge=T("Camera & FX · AR", "Camera & FX · AR")),
        ),

        split(
            id="ar-live",
            eyebrow=T("AR playback", "Trình diễn AR"),
            title=T("Press bars, a damper strip and a press light that fires once",
                    "Thanh nhấn, dải damper và một nhịp sáng chỉ bùng một lần"),
            ticks=[
                T("Live press bars are an independent toggle and off by default; they do not disable key tint. "
                  "A chevron-hidden Bar coverage slider (25–300% of the keys' depth) lets a bar's leading edge run "
                  "onto the keys — 100 stops at the keys, 200 reaches a white key's front edge, Keysight's full "
                  "coverage — and the flat bars and the 3D route honour it alike.",
                  "Live press bars là công tắc độc lập và mặc định tắt; bật nó không tắt key tint. Một thanh trượt "
                  "Bar coverage ẩn sau nút chevron (25–300% chiều sâu phím) cho đầu thanh chạy lên trên phím — 100 "
                  "là dừng ở phím, 200 chạm mép trước của phím trắng, tức full coverage kiểu Keysight — và cả "
                  "thanh phẳng lẫn đường 3D đều tuân theo."),
                T("Bar fade follows lifetime (also off by default) makes a bar's opacity walk with how far it has "
                  "stretched: Fade at birth and Fade at full length, 60% → 100% by default, so bars brighten as "
                  "they grow — and the fade walks backwards across the release.",
                  "Bar fade follows lifetime (cũng mặc định tắt) cho độ đặc của thanh thay đổi theo mức nó đã kéo "
                  "dài: Fade at birth và Fade at full length, mặc định 60% → 100%, nên thanh càng dài càng sáng — "
                  "và khi nhả phím, độ mờ đi ngược lại suốt quá trình nhả."),
                T("Every bar is retinted by the look's velocity colour through the press's true strength, and the "
                  "press light fires exactly once per press: the finger is the only source, so the falling head of "
                  "a live bar no longer re-flashes at touchdown on either note direction. The flash blooms in over "
                  "about 55 ms, brightness and size ride velocity over a wider band, and a long-held key breathes.",
                  "Mọi thanh được nhuộm lại theo màu velocity của look đúng với lực nhấn thật, và nhịp sáng chỉ "
                  "bùng đúng một lần cho mỗi lần nhấn: ngón tay là nguồn duy nhất, nên đầu thanh rơi không còn "
                  "bùng sáng lại khi chạm phím ở cả hai hướng nốt. Nhịp sáng loé lên trong khoảng 55 ms, độ sáng "
                  "và kích thước theo velocity rộng hơn, và một phím giữ lâu sẽ “thở” nhẹ."),
                T("From the AR Standard tier up, a glowing damper strip hugs the keys' back edge; the sustain "
                  "pedal (level 0..1) reaches it out over the fallboard and brightens it in the look's halo colour, "
                  "with its own on/off toggle and a Follow look / Custom colour switch in the AR PLAYBACK card.",
                  "Từ tier AR Standard trở lên, một dải damper phát sáng bám mép sau của phím; pedal sustain (mức "
                  "0..1) đẩy nó vươn ra ngoài thành đàn và làm nó sáng lên theo màu halo của look, kèm công tắc "
                  "bật/tắt riêng và lựa chọn màu Follow look / Custom trong thẻ AR PLAYBACK."),
            ],
            media=framed(doc, "stage-gpu-storm",
                         T("The notes and the effects, drawn over the camera in AR",
                           "Nốt và hiệu ứng, được vẽ đè lên camera trong AR"),
                         T("The same engine, the same effects — the AR overlay only changes where the keyboard "
                           "is on screen.",
                           "Cùng engine, cùng hiệu ứng — lớp phủ AR chỉ đổi chỗ bàn phím nằm trên màn hình."),
                         badge=T("GPU stage · Electric Storm", "Sân khấu GPU · Electric Storm")),
        ),

        split(
            id="align",
            flip=True,
            eyebrow=T("Staying aligned", "Giữ cho khớp"),
            title=T("The tools that tell you the tripod moved",
                    "Những công cụ cho bạn biết tripod đã xê dịch"),
            ticks=[
                T("Camera delay is stored per camera — the same key the calibration file uses, in ar-delay.json "
                  "beside the settings folder. A USB webcam is late by its own amount (roughly 60–150 ms) and a "
                  "virtual camera or a phone-as-webcam is very different, so each camera brings its own 0–300 ms "
                  "value back to the slider, and dragging it or accepting a MEASURE DELAY result writes to the "
                  "camera that is open.",
                  "Camera delay được lưu theo từng camera — cùng khoá mà tệp calibration dùng, trong ar-delay.json "
                  "cạnh thư mục cài đặt. Webcam USB có độ trễ riêng (khoảng 60–150 ms) và camera ảo hay điện "
                  "thoại làm webcam thì rất khác, nên mỗi camera mang giá trị 0–300 ms của nó trở lại thanh "
                  "trượt, và kéo thanh trượt hay nhận kết quả MEASURE DELAY đều ghi cho camera đang mở."),
                T("Alignment check redraws the saved key frame with octave lines over the live camera picture — "
                  "calibrated only, on every tier — so a bumped tripod or a keyboard that shifted shows up the "
                  "moment the lines drift off the real keys. Five high-contrast frame colours, machine-local, "
                  "never carried by presets or share codes.",
                  "Alignment check vẽ lại khung phím đã lưu kèm các đường quãng tám đè lên ảnh camera trực tiếp — "
                  "chỉ khi đã hiệu chỉnh, ở mọi tier — nên tripod bị đụng hay bàn phím bị xê dịch sẽ lộ ra ngay khi "
                  "đường kẻ lệch khỏi phím thật. Năm màu khung tương phản cao, chỉ thuộc máy này, không bao giờ đi "
                  "theo preset hay mã chia sẻ."),
                T("A drift watch, on by default, samples the key area about every two seconds and compares it with "
                  "the saved calibration; three straight readings past the threshold put a re-mark nudge on the AR "
                  "status line. Playing hands and lighting changes stay silent, and it never edits the calibration "
                  "itself.",
                  "Drift watch, mặc định bật, lấy mẫu vùng phím khoảng hai giây một lần và so với calibration đã "
                  "lưu; ba lần liên tiếp vượt ngưỡng sẽ đặt một nhắc nhở “đánh dấu lại” lên dòng trạng thái AR. "
                  "Bàn tay đang chơi và thay đổi ánh sáng không gây báo, và nó không bao giờ tự sửa calibration."),
                T("EXPORT CALIBRATION gathers every saved alignment of the camera in use — every view, picture size "
                  "and keyboard size — into one portable keyflow-ar-calibration JSON, and drops a snapshot PNG of "
                  "the camera's current frame beside it. IMPORT CALIBRATION restores them under the backup's own "
                  "camera link, pushing every row through the checks a fresh calibration passes: rows that fail are "
                  "counted and skipped, and no setting is touched.",
                  "EXPORT CALIBRATION gom mọi hiệu chỉnh đã lưu của camera đang dùng — mọi góc nhìn, cỡ hình và cỡ "
                  "bàn phím — vào một tệp JSON keyflow-ar-calibration gọn ghẽ, kèm ảnh PNG chụp khung camera hiện "
                  "tại bên cạnh. IMPORT CALIBRATION khôi phục chúng theo đúng liên kết camera trong bản sao lưu, "
                  "và đẩy từng dòng qua đúng các bước kiểm tra của một hiệu chỉnh mới: dòng không đạt bị đếm và bỏ "
                  "qua, và không cài đặt nào bị thay đổi."),
            ],
            media=framed(doc, "shortcuts",
                         T("The in-app keyboard and shortcuts card", "Thẻ bàn phím và phím tắt trong ứng dụng"),
                         T("The same F1 card that tells you how to play the stage — the AR tools all live in the "
                           "dock next to it.",
                           "Chính thẻ F1 chỉ bạn cách chơi sân khấu — còn các công cụ AR đều nằm trong dock ngay "
                           "cạnh đó."),
                         badge=T("Keyboard & shortcuts", "Bàn phím & phím tắt")),
        ),

        callout(
            style="tip",
            icon="info",
            title=T("Inside Calibrate, and under the hood", "Trong cửa sổ Calibrate, và bên dưới lớp áo"),
            body=[T("One line of camera tips answers the classic first-time mistakes — hang the camera over your "
                    "shoulder looking down the keys, avoid a very wide lens, keep your hands out of the picture "
                    "while marking — and a live Y′CbCr skin-lobe lookout samples the still it shows: a "
                    "skin-coloured share before the corners are down (anywhere in the picture) or after (only "
                    "inside the marked keys) quietly asks you to move your hands. It is advice, not a gate.",
                    "Một dòng gợi ý trong cửa sổ Calibrate trả lời những lỗi quen thuộc của lần đầu: treo camera "
                    "qua vai nhìn xuống phím, tránh ống kính quá rộng, và để tay ra khỏi khung khi đánh dấu — kèm "
                    "một bộ dò màu da Y′CbCr lấy mẫu ngay trên ảnh nó đang hiện: nếu có mảng màu da trước khi đặt "
                    "góc (bất kỳ đâu trong khung) hoặc sau khi đặt (chỉ trong vùng phím đã đánh dấu), dòng ghi chú "
                    "sẽ nhẹ nhàng nhắc bạn đưa tay ra. Đó là gợi ý, không phải rào chắn."),
                  T("The look retunes itself per camera view: on the leaned cameras the paper-thin effect lifts stay "
                    "at the catalogue's heights and the stand-up beams and arcs keep drawing, while the 90° "
                    "overhead view shrinks the lifts to 0.05 cm / 0.1 cm and leaves the stand-up quads home, because "
                    "they squash to a noise-thin hairline from straight above. If the GPU runs over budget, "
                    "ArQualityBudget drops effect families in a fixed order — particles, pulses, note lights, light "
                    "bars, note style, impact glow — and restores them as the pressure passes; keys, notes and "
                    "keypresses are never dropped.",
                    "Diện mạo tự chỉnh theo từng góc nhìn: với camera nghiêng, các hiệu ứng mỏng như giấy vẫn giữ "
                    "độ cao theo catalogue và các tia sáng dựng đứng vẫn được vẽ; còn góc nhìn 90° từ trên xuống "
                    "thu các độ nâng về 0,05 cm / 0,1 cm và bỏ luôn các quad dựng đứng, vì nhìn thẳng từ trên chúng "
                    "bị ép thành một sợi chỉ nhiễu. Nếu GPU vượt ngân sách, ArQualityBudget bỏ dần các nhóm hiệu "
                    "ứng theo thứ tự cố định — hạt, xung, đèn nốt, thanh sáng, kiểu nốt, sáng va chạm — và trả lại "
                    "khi áp lực qua đi; phím, nốt và nhịp nhấn không bao giờ bị bỏ.")],
        ),

        split(
            id="hands",
            eyebrow=T("Hand tracking", "Theo dõi bàn tay"),
            title=T("Which key is your hand over? The stage knows",
                    "Bàn tay bạn đang ở phím nào? Sân khấu biết"),
            ticks=[
                T("Hand tracking reads your hand out of the camera frame itself: skin pixels are found by colour "
                  "(YCbCr) and the largest group of neighbouring skin cells is taken as the hand. No model, no "
                  "download, no network.",
                  "Theo dõi bàn tay đọc bàn tay từ chính khung camera: pixel nào là da thì được tìm theo màu "
                  "(YCbCr), và nhóm ô da liền kề lớn nhất được coi là bàn tay. Không mô hình, không tải thêm, "
                  "không mạng."),
                T("It counts the fingers you raise and marks the key your hand is over with a light bar on that key, "
                  "a position dot, and one dot per finger.",
                  "Nó đếm số ngón đang giơ và đánh dấu phím bàn tay đang ở trên bằng một dải sáng trên phím, một "
                  "chấm vị trí và một chấm cho mỗi ngón."),
                T("The camera stays open for this layer even when the camera picture itself is hidden — so you can "
                  "have the markers without your face on the stage.",
                  "Camera vẫn được mở cho lớp này ngay cả khi ảnh camera đang ẩn — nên bạn có điểm đánh dấu mà "
                  "không cần đưa mặt mình lên sân khấu."),
                T("Skin sensitivity is a slider, and the status line reports the finger count, the key and the "
                  "percentage of the frame your hand fills.",
                  "Skin sensitivity là một thanh trượt, và dòng trạng thái báo số ngón, phím cùng phần trăm khung "
                  "hình mà bàn tay chiếm."),
            ],
            media=framed(doc, "play-dialog",
                         T("The session dialog, where the score and the stage layers meet",
                           "Hộp thoại phiên, nơi bản nhạc gặp các lớp sân khấu"),
                         T("Hand tracking draws on the stage itself; the session dialog is where the song and the "
                           "stage layers are chosen.",
                           "Theo dõi bàn tay vẽ ngay trên sân khấu; hộp thoại phiên là nơi chọn bài và các lớp "
                           "sân khấu."),
                         badge=T("Session", "Phiên")),
        ),

        steps(
            id="recipe",
            cols=4,
            eyebrow=T("Two recipes", "Hai công thức"),
            title=T("The “player cut out of the background” look, and the “stage on my piano” look",
                    "Kiểu cảnh “người chơi tách khỏi nền”, và kiểu “sân khấu trên cây đàn của tôi”"),
            items=[
                {"t": T("Film against green", "Quay trên nền xanh"),
                 "d": T("Use a green backdrop behind you; the key tolerance removes exactly that green.",
                        "Dùng phông xanh lá sau lưng bạn; dung sai key sẽ loại bỏ đúng màu xanh đó.")},
                {"t": T("Or key the stage instead", "Hoặc key chính sân khấu"),
                 "d": T("Choose the Green Screen preset and composite the whole stage over your own footage in OBS.",
                        "Chọn preset Green Screen rồi ghép toàn bộ sân khấu đè lên cảnh quay của bạn trong OBS.")},
                {"t": T("Mark four corners once", "Đánh dấu bốn góc một lần"),
                 "d": T("Hang the camera over your shoulder, mark the four corners of the key strip, and the AR "
                        "overlay draws the notes onto your real keys from then on.",
                        "Treo camera qua vai, đánh dấu bốn góc của dải phím, và từ đó lớp phủ AR vẽ nốt lên chính "
                        "phím thật của bạn.")},
                {"t": T("Keep it honest", "Giữ cho khớp"),
                 "d": T("LEAVE Alignment check on so the frame lines tell you the moment the tripod moves, and "
                        "export the calibration before you move the camera to another room.",
                        "Bật Alignment check để khung kẻ cho bạn biết ngay khi tripod xê dịch, và xuất "
                        "calibration trước khi mang camera sang phòng khác.")},
            ],
        ),

        table(
            id="settings",
            eyebrow=T("Camera & FX page", "Trang Camera & FX"),
            title=T("Everything on one page of the dock", "Tất cả trên một trang của bàn thiết kế"),
            head=[T("Card", "Thẻ"), T("Controls", "Điều khiển")],
            rows=[
                [E("Camera & FX"),
                 T("Parallax, zoom, frame, saturation, contrast and bloom for the stage itself.",
                   "Parallax, zoom, khung hình, bão hoà, tương phản và bloom cho chính sân khấu.")],
                [E("WEBCAM OVERLAY"),
                 T("Camera overlay switch, the machine's own camera list with REFRESH CAMERAS, USE CAMERA / "
                   "CHOOSE VIDEO…, Corner, Size, Opacity, Mirror, Key tolerance and a status line with the real "
                   "mode.",
                   "Công tắc Camera overlay, danh sách camera của chính máy với REFRESH CAMERAS, USE CAMERA / "
                   "CHOOSE VIDEO…, Corner, Size, Opacity, Mirror, Key tolerance và dòng trạng thái kèm mode thật.")],
                [E("AR OVERLAY"),
                 T("AR overlay switch, camera view, Calibrate (four corners, Move/Rotate/Scale gizmo, numeric "
                   "translation and scale, camera tips and the skin lookout), Notes in perspective, the note-"
                   "direction controls, Quality (Lite / Standard / Ultra) and Camera delay.",
                   "Công tắc AR overlay, góc nhìn camera, Calibrate (bốn góc, gizmo Move/Rotate/Scale, thanh số "
                   "cho tịnh tiến và scale, gợi ý camera và bộ dò màu da), Notes in perspective, các điều khiển "
                   "hướng nốt, Quality (Lite / Standard / Ultra) và Camera delay.")],
                [E("AR PLAYBACK"),
                 T("Live press bars, Bar coverage (25–300%), Bar fade follows lifetime with Fade at birth and "
                   "Fade at full length, and the damper strip with its colour choice.",
                   "Live press bars, Bar coverage (25–300%), Bar fade follows lifetime với Fade at birth và Fade "
                   "at full length, cùng dải damper và lựa chọn màu của nó.")],
                [E("KEYBOARD ALIGNMENT"),
                 T("Alignment check with five frame colours, the drift watch, EXPORT CALIBRATION and IMPORT "
                   "CALIBRATION — all of it machine-local.",
                   "Alignment check với năm màu khung, drift watch, EXPORT CALIBRATION và IMPORT CALIBRATION — "
                   "tất cả chỉ thuộc máy này.")],
                [E("HAND TRACKING"),
                 T("Hand tracking switch, Skin sensitivity, and a status line with the finger count, the key and the "
                   "share of the frame the hand fills.",
                   "Công tắc Hand tracking, thanh Skin sensitivity, và dòng trạng thái ghi số ngón, phím cùng phần "
                   "trăm khung hình bàn tay chiếm.")],
            ],
        ),

        callout(
            style="warn",
            icon="alert",
            title=T("Honest about what classical vision and a webcam can do",
                    "Nói thẳng về giới hạn của thị giác cổ điển và một chiếc webcam"),
            body=[
                T("Hand tracking is classical computer vision, not a machine-learning model. With two hands in view, "
                  "or a backdrop close to skin colour, only the biggest hand is followed; the finger count is only "
                  "trustworthy when the hand is large enough in the frame; and it wants a simple, reasonably lit "
                  "background.",
                  "Theo dõi bàn tay là thị giác máy tính cổ điển, không phải mô hình học máy. Khi có hai bàn tay "
                  "trong khung, hoặc nền trùng màu da, chỉ bàn tay lớn nhất được theo; số ngón chỉ đáng tin khi bàn "
                  "tay đủ lớn trong khung; và nó cần một nền đơn giản, đủ sáng."),
                T("The AR overlay is the newest part of the app and it says so: it has automated regression coverage "
                  "(the render path is re-projected on WARP on every build), but it has not been tried on a real "
                  "webcam yet, full setting/value parity with the flat stage is not claimed, and the ambient layers "
                  "— petals, shooting stars — stay flat screen-space rather than following the perspective. Stage-"
                  "space falling trails are suppressed over the camera, and the camera is the machine's: applying a "
                  "preset or pasting a share code never changes the camera you picked.",
                  "Lớp phủ AR là phần mới nhất của ứng dụng và nó nói thẳng điều đó: đã có kiểm thử hồi quy tự động "
                  "(đường render được chiếu lại trên WARP mỗi lần build), nhưng chưa từng thử với webcam thật, "
                  "chưa cam kết đủ mọi cài đặt/giá trị như sân khấu phẳng, và các lớp ambient — cánh hoa, sao băng "
                  "— vẫn phẳng theo màn hình chứ không theo phối cảnh. Vệt rơi trong không gian sân khấu bị bỏ khi "
                  "đè lên camera, và camera thuộc về máy này: áp preset hay dán mã chia sẻ không bao giờ đổi camera "
                  "bạn đã chọn."),
                T("Nothing is uploaded — frames are read locally, drawn locally and never leave the machine.",
                  "Không có gì được tải lên — khung hình được đọc tại máy, vẽ tại máy và không bao giờ rời khỏi "
                  "máy."),
            ],
        ),

        pagenav(prev=("features/design.html", "design"), next=("gallery.html", "gallery")),
        cta(
            title=T("One camera, one cable, one stage", "Một chiếc camera, một sợi cáp, một sân khấu"),
            sub=T("The overlay, the AR calibration and hand tracking are in the same free download as everything "
                  "else.",
                  "Lớp phủ camera, hiệu chỉnh AR và theo dõi bàn tay nằm trong cùng bản tải miễn phí với mọi thứ "
                  "khác."),
            actions=[DOWNLOAD,
                     {"label": T("Open the gallery", "Mở thư viện ảnh"), "href": "gallery.html",
                      "kind": "btn-ghost", "icon": "image"}],
        ),
    ]
    return {
        "title": T("Camera overlay, AR overlay & hand tracking · Keyflow",
                   "Lớp phủ camera, lớp phủ AR & theo dõi bàn tay · Keyflow"),
        "description": T(
            "Draw a live webcam or a looping video onto the Keyflow stage in any corner, key out a green backdrop, "
            "switch on hand tracking that reads your hands from the camera frame with classical computer vision, or "
            "calibrate the AR overlay and watch the notes fall onto your own keyboard — no model to download, "
            "nothing uploaded.",
            "Vẽ webcam trực tiếp hoặc video lặp lên sân khấu Keyflow ở bất kỳ góc nào, key nền xanh lá, bật theo "
            "dõi bàn tay đọc tay bạn ngay từ khung camera bằng thị giác máy tính cổ điển, hoặc hiệu chỉnh lớp phủ "
            "AR để xem nốt rơi xuống chính cây đàn của bạn — không phải tải mô hình, không gì được tải lên."),
        "og_image": "previews/en/stage-live.png",
        "crumb_trail": TRAIL + [("Camera & hand tracking", "features/camera.html")],
        "body": body,
    }
