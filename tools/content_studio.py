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
                T("No SoundFont loaded means picture only, and the status line says so before you press REC.",
                  "Máy chưa nạp SoundFont thì chỉ ghi hình, và dòng thông tin nói rõ trước khi bạn bấm REC."),
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
                T("The info line adapts to the machine: with a SoundFont it says where the sound goes, without one "
                  "it says plainly that the take will be silent.",
                  "Dòng thông tin đổi theo thực tế từng máy: có SoundFont thì nói rõ đường tiếng đi đâu, không có "
                  "thì nói thẳng rằng bản ghi sẽ không có tiếng."),
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
    ("Neon Violet", T("The default: a dark hall, violet neon and clean trails.",
                      "Mặc định: hội trường tối, neon tím và vệt sáng gọn.")),
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
    ("Concert Gold", T("Champagne gold on ebony, matched to the Concert Grand interface.",
                       "Vàng champagne trên nền gỗ đen, hợp với giao diện Concert Grand.")),
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
                E("KEYFLOW-LOOK-1:…"),
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
                    (E("Audio"), T("Load a SoundFont, choose an instrument preset, toggle the hall reverb.",
                                   "Nạp SoundFont, chọn preset nhạc cụ, bật/tắt hall reverb.")),
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
                         T("The start menu: Perform & Play, Quick Adjustments for the most-used controls, Stage "
                           "Design Studio for the full dock, and the language chips.",
                           "Menu khởi động: Perform & Play, Quick Adjustments cho các điều khiển hay dùng, Stage "
                           "Design Studio cho bàn thiết kế đầy đủ, và chip chọn ngôn ngữ."),
                         badge=T("Concert Grand menu", "Menu Concert Grand")),
        ),

        split(
            id="share",
            eyebrow=T("Share codes", "Mã chia sẻ"),
            title=T("COPY CODE, paste it in a chat, APPLY CODE",
                    "COPY CODE, dán vào khung chat, rồi APPLY CODE"),
            ticks=[
                T("A code is the whole look — every visual setting — gzipped into base64url behind a "
                  "KEYFLOW-LOOK-1: version prefix, so one line of text carries it.",
                  "Một mã chia sẻ là toàn bộ diện mạo — mọi cài đặt hình ảnh — nén gzip rồi mã hoá base64url sau "
                  "tiền tố phiên bản KEYFLOW-LOOK-1:, nên chỉ một dòng chữ là mang đi được."),
                T("It round-trips every value but deliberately drops the sender's background image path: a look that "
                  "used a picture falls back to a solid colour rather than pointing at a file you do not have.",
                  "Mã đi-về đúng từng giá trị nhưng cố ý bỏ đường dẫn ảnh nền của máy người gửi: diện mạo dùng ảnh "
                  "sẽ rơi về nền màu thay vì trỏ tới một tệp bạn không có."),
                T("A code that a chat window wrapped over several lines still reads.",
                  "Mã bị cửa sổ chat xuống dòng vẫn đọc được."),
                T("An empty, unknown, other-version, oversized or corrupt code is rejected with the reason printed "
                  "right in the dock — and your current settings are left alone.",
                  "Mã rỗng, lạ, khác phiên bản, quá lớn hoặc hỏng bị từ chối kèm lý do in ngay trong dock — và cài "
                  "đặt hiện tại của bạn được giữ nguyên."),
            ],
            media=_codecard(
                doc, "share",
                T("What a shared look looks like", "Một diện mạo được chia sẻ trông ra sao"),
                "KEYFLOW-LOOK-1:H4sIAAAAAAAACqvWKkktLlGy\n"
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
            title=T("Put yourself on the stage — and let it know where your hands are",
                    "Đưa bạn lên sân khấu — và cho nó biết tay bạn đang ở đâu"),
            lead=T("Draw a live webcam or a looping video file onto the stage in any corner, key out a green "
                   "backdrop, and turn on hand tracking: Keyflow reads your hands straight out of the camera frame "
                   "with classical computer vision — no model, no download, nothing leaves your machine.",
                   "Vẽ một webcam trực tiếp hoặc một tệp video chạy lặp lên sân khấu ở bất kỳ góc nào, key nền "
                   "xanh, và bật theo dõi bàn tay: Keyflow đọc bàn tay ngay từ khung camera bằng thị giác máy tính "
                   "cổ điển — không mô hình, không tải gì thêm, không gì rời khỏi máy bạn."),
            chips=[
                T("Live camera or video file", "Camera trực tiếp hoặc tệp video"),
                T("4 corners · 15–60% width", "4 góc · 15–60% chiều rộng"),
                T("Green key, 0–100 tolerance", "Key xanh, dung sai 0–100"),
                T("Hand tracking, no ML model", "Theo dõi tay, không mô hình ML"),
                E("30 fps overlay"),
            ],
            shot="stage-live",
            alt=T("The live stage where the camera overlay is drawn",
                  "Sân khấu live nơi lớp phủ camera được vẽ"),
            cap=T("The live stage: the camera overlay is composited into a corner of this same frame, and the hand "
                  "marker sits on the keys themselves.",
                  "Sân khấu live: lớp phủ camera được ghép vào một góc của chính khung hình này, còn điểm đánh dấu "
                  "bàn tay nằm ngay trên phím."),
            badge=E("Camera & FX"),
        ),

        band(stats=[
            (("30", "30"), T("fps the overlay reaches the stage at", "fps lớp phủ lên sân khấu"), 30),
            (("4", "4"), T("corners to place it in", "góc để đặt khung camera"), 4),
            (("15–60%", "15–60%"), T("of the stage width", "chiều rộng sân khấu"), None),
            (("0", "0"), T("models to download", "mô hình phải tải về"), 0),
        ]),

        split(
            id="overlay",
            eyebrow=T("Webcam overlay", "Lớp phủ webcam"),
            title=T("A camera window on the stage, keyed if you want it",
                    "Một cửa sổ camera trên sân khấu, key nền nếu bạn muốn"),
            ticks=[
                T("Camera overlay draws a live camera or a looping video file onto the stage as a small window. "
                  "Pick a camera from the list your machine has (REFRESH CAMERAS re-reads it), or USE CAMERA / "
                  "CHOOSE VIDEO… to change the source.",
                  "Camera overlay vẽ một camera trực tiếp hoặc một tệp video chạy lặp lên sân khấu như một cửa sổ "
                  "nhỏ. Chọn camera trong danh sách máy đang có (REFRESH CAMERAS đọc lại), hoặc USE CAMERA / "
                  "CHOOSE VIDEO… để đổi nguồn."),
                T("Corner places it in any of the four corners, Size sets 15–60% of the stage width, and Opacity and "
                  "Mirror do what they say.",
                  "Corner đặt khung vào một trong bốn góc, Size chỉnh 15–60% chiều rộng sân khấu, còn Opacity và "
                  "Mirror đúng như tên gọi."),
                T("Key tolerance goes from 0 (key off) to 100 (widest) and removes pure green — exactly the colour of "
                  "the Green Screen preset — so the backdrop disappears and the player stays.",
                  "Key tolerance chạy từ 0 (tắt key) tới 100 (rộng nhất) và loại bỏ màu xanh lá thuần — đúng màu "
                  "của preset Green Screen — nên phông xanh biến mất còn người chơi ở lại."),
                T("The status line under the rows says plainly which camera is open, which file is playing, or why it "
                  "cannot run: no camera on this machine, or no Media Foundation.",
                  "Dòng trạng thái dưới các hàng nói rõ đang mở camera nào, đang chạy tệp nào, hay vì sao không "
                  "chạy được: máy không có camera, hoặc máy không có Media Foundation."),
                T("Frames are read with Media Foundation on a thread of their own and reach the stage at 30 fps, so "
                  "the camera never blocks drawing.",
                  "Khung hình được đọc bằng Media Foundation trên luồng riêng và lên sân khấu ở 30 fps, nên camera "
                  "không bao giờ chặn việc vẽ."),
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
            id="hands",
            flip=True,
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
            media=framed(doc, "shortcuts",
                         T("The keyboard and shortcuts card", "Thẻ bàn phím và phím tắt"),
                         T("The in-app F1 card: playing the stage with the computer keys, moving around, and the "
                           "session and capture controls.",
                           "Thẻ F1 trong ứng dụng: chơi sân khấu bằng phím máy tính, điều hướng, và các điều khiển "
                           "phiên cùng ghi hình."),
                         badge=T("Keyboard & shortcuts", "Bàn phím & phím tắt")),
        ),

        steps(
            id="recipe",
            cols=4,
            eyebrow=T("A recipe", "Một công thức"),
            title=T("The “player cut out of the background” look",
                    "Kiểu cảnh “người chơi tách khỏi nền”"),
            items=[
                {"t": T("Film against green", "Quay trên nền xanh"),
                 "d": T("Use a green backdrop behind you; the key tolerance removes exactly that green.",
                        "Dùng phông xanh lá sau lưng bạn; dung sai key sẽ loại bỏ đúng màu xanh đó.")},
                {"t": T("Or key the stage instead", "Hoặc key chính sân khấu"),
                 "d": T("Choose the Green Screen preset and composite the whole stage over your own footage in OBS.",
                        "Chọn preset Green Screen rồi ghép toàn bộ sân khấu đè lên cảnh quay của bạn trong OBS.")},
                {"t": T("Place and size it", "Đặt vị trí và kích thước"),
                 "d": T("Corner, Size and Opacity put the camera window where your composition wants it.",
                        "Corner, Size và Opacity đặt cửa sổ camera đúng chỗ bố cục của bạn cần.")},
                {"t": T("Markers without your face", "Có điểm đánh dấu, không cần mặt bạn"),
                 "d": T("Hide the camera picture and leave hand tracking on for the key markers alone.",
                        "Ẩn ảnh camera và vẫn bật theo dõi bàn tay để chỉ lấy các điểm đánh dấu trên phím.")},
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
                 T("Camera overlay switch, camera list with REFRESH CAMERAS, USE CAMERA / CHOOSE VIDEO…, Corner, "
                   "Size, Opacity, Mirror, Key tolerance and a status line.",
                   "Công tắc Camera overlay, danh sách camera với REFRESH CAMERAS, USE CAMERA / CHOOSE VIDEO…, "
                   "Corner, Size, Opacity, Mirror, Key tolerance và một dòng trạng thái.")],
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
            title=T("Honest about what classical vision can do", "Nói thẳng về giới hạn của thị giác cổ điển"),
            body=[
                T("Hand tracking is classical computer vision, not a machine-learning model. With two hands in view, "
                  "or a backdrop close to skin colour, only the biggest hand is followed; the finger count is only "
                  "trustworthy when the hand is large enough in the frame; and it wants a simple, reasonably lit "
                  "background.",
                  "Theo dõi bàn tay là thị giác máy tính cổ điển, không phải mô hình học máy. Khi có hai bàn tay "
                  "trong khung, hoặc nền trùng màu da, chỉ bàn tay lớn nhất được theo; số ngón chỉ đáng tin khi bàn "
                  "tay đủ lớn trong khung; và nó cần một nền đơn giản, đủ sáng."),
                T("There is no 3D perspective camera either: the stage is a flat piano roll with slight parallax. "
                  "Nothing is uploaded — frames are read locally, drawn locally and never leave the machine.",
                  "Cũng chưa có camera phối cảnh 3D: sân khấu là piano roll phẳng với parallax nhẹ. "
                  "Không có gì được tải lên — khung hình được đọc tại máy, vẽ tại máy và không bao giờ rời khỏi máy."),
            ],
        ),

        pagenav(prev=("features/design.html", "design"), next=("gallery.html", "gallery")),
        cta(
            title=T("One camera, one cable, one stage", "Một chiếc camera, một sợi cáp, một sân khấu"),
            sub=T("The overlay and hand tracking are in the same free download as everything else.",
                  "Lớp phủ camera và theo dõi bàn tay nằm trong cùng bản tải miễn phí với mọi thứ khác."),
            actions=[DOWNLOAD,
                     {"label": T("Open the gallery", "Mở thư viện ảnh"), "href": "gallery.html",
                      "kind": "btn-ghost", "icon": "image"}],
        ),
    ]
    return {
        "title": T("Camera overlay & hand tracking · Keyflow",
                   "Lớp phủ camera & theo dõi bàn tay · Keyflow"),
        "description": T(
            "Draw a live webcam or a looping video onto the Keyflow stage in any corner, key out a green backdrop, "
            "and switch on hand tracking that reads your hands from the camera frame with classical computer vision "
            "— no model to download, nothing uploaded.",
            "Vẽ webcam trực tiếp hoặc video lặp lên sân khấu Keyflow ở bất kỳ góc nào, key nền xanh lá, và bật theo "
            "dõi bàn tay đọc tay bạn ngay từ khung camera bằng thị giác máy tính cổ điển — không phải tải mô hình, "
            "không gì được tải lên."),
        "og_image": "previews/en/stage-live.png",
        "crumb_trail": TRAIL + [("Camera & hand tracking", "features/camera.html")],
        "body": body,
    }
