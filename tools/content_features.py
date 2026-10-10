#!/usr/bin/env python3
"""Feature pages, part one: the stage, practice, and sound & MIDI.

Each builder returns one page spec.  The copy is condensed from the Keyflow
release repository's README (English and Vietnamese editions) so the site and
the documentation describe the same product.
"""
from __future__ import annotations

from sitekit import (E, REPO, T, band, callout, chipcloud, cta, framed, grid, iconbox,
                     pagehero, pagenav, slider, split, specdl, steps, table)

DOWNLOAD = {"label": T("Download for Windows", "Tải cho Windows"), "href": "download.html",
            "kind": "btn-gold", "icon": "download"}


def feature_hero(doc, *, crumb, eyebrow, title, lead, chips, shot, alt, cap, badge=None):
    """The header every feature page shares: breadcrumb, copy, one picture."""
    return pagehero(
        crumbs=[(T("Features", "Tính năng"), "index.html#features")],
        crumb=crumb, eyebrow=eyebrow, title=title, lead=lead,
        chips=[(c, "gold") for c in chips],
        actions=[DOWNLOAD,
                 {"label": T("All features", "Tất cả tính năng"), "href": "index.html#features",
                  "kind": "btn-ghost", "icon": "grid"}],
        media=framed(doc, shot, alt, cap, badge=badge, lazy=False),
    )


TRAIL = [("Features", "index.html#features")]


# ===========================================================================
# 1. GPU stage & VFX
# ===========================================================================
def build_stage(doc) -> dict:
    body = [
        feature_hero(
            doc,
            crumb=T("GPU stage & VFX", "Sân khấu GPU & hiệu ứng"),
            eyebrow=T("The visual engine", "Engine đồ hoạ"),
            title=T("A Direct3D 11 stage that never holds up your MIDI",
                    "Sân khấu Direct3D 11 không bao giờ giữ chân MIDI"),
            lead=T("The stage runs a game loop of its own on a thread of its own: 16-bit HDR, multi-level bloom, "
                   "up to 24,000 particles and an 88-key keyboard shaded by HLSL. A heavy frame costs frame rate — "
                   "never latency, because your notes reach the sound engine and the renderer on the MIDI callback "
                   "thread itself.",
                   "Sân khấu chạy một vòng lặp game riêng trên một luồng riêng: HDR 16-bit, bloom nhiều tầng, "
                   "tới 24.000 hạt và bàn phím 88 phím đổ bóng bằng HLSL. Khung hình nặng chỉ tốn FPS — "
                   "không bao giờ trễ, vì nốt nhạc đi tới engine âm thanh và bộ dựng hình ngay trên luồng "
                   "callback MIDI."),
            chips=[
                E("Direct3D 11 · Vortice.Windows"), E("HDR 16-bit + bloom"),
                T("60 / 120 / 144 / 240 FPS", "60 / 120 / 144 / 240 FPS"),
                E("HLSL · ACES filmic"), T("WARP & WPF fallback", "Dự phòng WARP & WPF"),
            ],
            shot="stage-gpu-galaxy",
            alt=T("The GPU stage running the Galaxy Voyage preset",
                  "Sân khấu GPU đang chạy preset Galaxy Voyage"),
            cap=T("Galaxy Voyage, drawn by the GPU engine: rainbow trails, a cosmic ambient layer and the lit keyboard.",
                  "Galaxy Voyage do engine GPU vẽ: vệt cầu vồng, lớp nền vũ trụ và bàn phím được chiếu sáng."),
            badge=T("Rendered in-app", "Render trong ứng dụng"),
        ),

        band(stats=[
            (("240", "240"), T("FPS target on the GPU stage", "FPS mục tiêu trên sân khấu GPU"), 240),
            (("24,000", "24.000"), T("particles in one frame", "hạt trong một khung hình"), None),
            (("12", "12"), T("HLSL shader entry points", "entry point shader HLSL"), 12),
            (("6 + 6", "6 + 6"), T("shader backgrounds and hit-line styles", "nền shader và kiểu đường chạm"), None),
        ]),

        split(
            id="engine",
            eyebrow=T("The render loop", "Vòng lặp vẽ"),
            title=T("Why the picture can be heavy and the playing still light",
                    "Vì sao hình ảnh có thể nặng mà việc chơi vẫn nhẹ"),
            ticks=[
                T("One game loop on its own thread owns the ID3D11Device and its context, at 60, 120, 144, 240 FPS "
                  "or unlimited — 144 by default.",
                  "Một vòng lặp game trên luồng riêng sở hữu ID3D11Device và context của nó, ở mức 60, 120, 144, "
                  "240 FPS hoặc không giới hạn — mặc định 144."),
                T("MIDI input goes to the synthesizer and to the GPU engine on the callback thread, so notes and "
                  "pedals keep the order they arrived in and never wait for the UI dispatcher.",
                  "Tín hiệu MIDI đi tới bộ tổng hợp âm thanh và engine GPU ngay trên luồng callback, nên nốt và "
                  "pedal giữ đúng thứ tự đến và không phải chờ dispatcher của giao diện."),
                T("The render thread receives the running song, the held keys and a clock extrapolated by never "
                  "more than 50 ms.",
                  "Luồng vẽ nhận bài đang chạy, các phím đang giữ và một đồng hồ ngoại suy không bao giờ quá 50 ms."),
                T("OPEN GPU STAGE WINDOW opens a flip-model swap-chain window with optional VSync and F11 full "
                  "screen — for a second monitor, a projector or OBS.",
                  "OPEN GPU STAGE WINDOW mở một cửa sổ swap chain flip-model, VSync tuỳ chọn và F11 toàn màn hình — "
                  "dành cho màn hình thứ hai, máy chiếu hoặc OBS."),
                T("If Direct3D cannot start, the WPF renderer takes over and General → GRAPHICS ENGINE says why; a "
                  "machine with no compatible card uses WARP — the same shaders, just slower.",
                  "Nếu Direct3D không khởi động được, bộ dựng hình WPF thay thế và trang General → GRAPHICS ENGINE "
                  "nói rõ lý do; máy không có card tương thích sẽ dùng WARP — cùng shader, chỉ chậm hơn."),
            ],
            actions=[{"label": T("Graphics settings in the guide", "Cài đặt đồ hoạ trong hướng dẫn"),
                      "href": "guide.html#setup", "kind": "btn-ghost", "icon": "sliders"}],
            media=framed(doc, "stage-gpu-storm",
                         T("Electric Storm: speed lines and arcs between held keys",
                           "Electric Storm: vệt tốc độ và tia điện giữa các phím đang giữ"),
                         T("Electric Storm: the same engine, a different effect family — speed-line trails and "
                           "electric arcs joining the keys you hold.",
                           "Electric Storm: cùng engine, họ hiệu ứng khác — vệt tốc độ và tia điện nối những "
                           "phím bạn giữ."),
                         badge=T("GPU stage · Electric Storm", "Sân khấu GPU · Electric Storm")),
        ),

        grid(
            id="effects",
            eyebrow=T("Effect families", "Các họ hiệu ứng"),
            title=T("Every family of the software engine runs on the GPU",
                    "Mọi họ hiệu ứng của engine phần mềm đều chạy trên GPU"),
            cards=[
                {"icon": "spark", "t": T("Falling trails", "Vệt rơi"),
                 "d": T("Glow, Sparkles, Speed lines, Blur, Ribbon, Rainbow and Stream, plus ghosting behind the note.",
                        "Glow, Sparkles, Speed lines, Blur, Ribbon, Rainbow và Stream, kèm bóng ma phía sau nốt.")},
                {"icon": "loop", "t": T("Hold effects", "Hiệu ứng giữ phím"),
                 "d": T("A bar, a breath, a vibration or an electric arc joining the keys you keep down.",
                        "Thanh giữ, nhịp thở, rung hoặc tia điện nối những phím bạn đang giữ.")},
                {"icon": "wand", "t": T("Release effects", "Hiệu ứng nhả phím"),
                 "d": T("Six ways for a note to leave the stage when you let go of the key.",
                        "Sáu cách một nốt rời sân khấu khi bạn nhả phím.")},
                {"icon": "bolt", "t": T("Impact waves & flashes", "Sóng va chạm & chớp"),
                 "d": T("Ring, Shockwave or Ripple, with Flash, Lightning or Plasma driven by how hard the note was hit.",
                        "Ring, Shockwave hoặc Ripple, cùng Flash, Lightning hay Plasma theo lực nhấn của nốt.")},
                {"icon": "flame", "t": T("Bursts & morphs", "Nổ hạt & biến hình"),
                 "d": T("Five particle bursts and five note morphs — Shatter, Melt, Absorb, Bounce and Star.",
                        "Năm kiểu nổ hạt và năm kiểu biến hình nốt — Shatter, Melt, Absorb, Bounce và Star.")},
                {"icon": "layers", "t": T("Ambient layers", "Lớp không khí"),
                 "d": T("Energy, Nature, Light and Cosmic, each switchable on its own, plus acoustic motes, guide "
                        "lanes and pedal glow.",
                        "Energy, Nature, Light và Cosmic, mỗi lớp bật/tắt riêng, cùng bụi acoustic, guide lanes "
                        "và pedal glow.")},
            ],
        ),

        table(
            id="notes",
            eyebrow=T("Notes", "Nốt nhạc"),
            title=T("Every note parameter, on one page", "Mọi thông số của nốt, trên một trang"),
            head=[T("Group", "Nhóm"), T("What you can set", "Bạn chỉnh được gì")],
            rows=[
                [T("Style", "Kiểu nốt"),
                 T("Four: Solid, Neon outline, Glass, and Fire with an animated burning texture.",
                   "Bốn kiểu: Solid, Neon outline, Glass, và Fire có vân cháy chuyển động.")],
                [T("Colour", "Màu sắc"),
                 T("Five modes: gradient by pitch (six palettes or custom start/end colours), by hand with a movable "
                   "split point, by MIDI track with an eight-colour table, rainbow by pitch and rainbow by time.",
                   "Năm chế độ: gradient theo cao độ (sáu palette hoặc màu đầu–cuối tuỳ chọn), theo tay với điểm "
                   "chia đổi được, theo track MIDI với bảng tám màu, cầu vồng theo cao độ và cầu vồng theo thời gian.")],
                [T("Shape", "Hình dáng"),
                 T("Width, corner radius, minimum length, gap between notes, 3D shadow, the note name printed on the "
                   "bar, tint, bloom, border brightness and thickness, leading-edge glow and refraction.",
                   "Độ rộng, bo góc, độ dài tối thiểu, khe hở giữa các nốt, đổ bóng 3D, tên nốt in trên thanh, "
                   "tint, bloom, độ sáng và độ dày viền, glow cạnh trước và khúc xạ.")],
                [T("Motion", "Chuyển động"),
                 T("Fall speed and direction — Down falls to the keys and sinks under the hit line, Up is born at the "
                   "key with the note and rises out of the stage — plus shimmer and landing glow on the GPU stage.",
                   "Tốc độ rơi và hướng — Down rơi xuống chạm phím rồi chìm dưới đường chạm, Up sinh ra tại phím "
                   "theo tiếng nốt rồi bốc lên khỏi sân khấu — cùng shimmer và landing glow trên sân khấu GPU.")],
                [T("Smart modulators", "Bộ điều biến thông minh"),
                 T("Velocity, octave, keyboard zone, pedal, tempo and audio reactivity feed the effects.",
                   "Velocity, quãng tám, vùng bàn phím, pedal, tempo và phản ứng theo âm thanh đều đưa vào hiệu ứng.")],
            ],
            note=T("All of it lives on the Notes page of the design dock, and every change applies live.",
                   "Tất cả nằm ở trang Notes của bàn thiết kế, và mọi thay đổi áp dụng ngay lập tức."),
        ),

        split(
            id="keyboard",
            flip=True,
            eyebrow=T("Ray-traced keyboard", "Bàn phím ray-tracing"),
            title=T("Eighty-eight keys shaded like a product render",
                    "Tám mươi tám phím đổ bóng như render sản phẩm"),
            body=[T("The keyboard is drawn by a shader, not a bitmap: a Cook-Torrance GGX BRDF with Smith visibility "
                    "and Schlick fresnel, a softbox with a real penumbra, contact occlusion inside the gaps between "
                    "keys, image-based lighting from the environment, coloured light thrown back by the keys that "
                    "are sounding, and an ACES filmic tonemap.",
                    "Bàn phím được vẽ bằng shader chứ không phải ảnh: BRDF Cook-Torrance GGX với Smith visibility "
                    "và Schlick fresnel, softbox có vùng nửa tối thật, che khuất tiếp xúc trong khe phím, ánh sáng "
                    "môi trường IBL, ánh sáng màu hắt lại từ phím đang kêu, và tonemap ACES filmic.")],
            ticks=[
                T("Key styles Classic, Studio 3D and Glass, with key height, black-key length, key labels, lid "
                  "shadow, the red felt strip and how far a key dips when pressed.",
                  "Kiểu phím Classic, Studio 3D và Glass, cùng chiều cao phím, độ dài phím đen, nhãn phím, "
                  "bóng nắp đàn, dải nỉ đỏ và độ lún khi nhấn."),
                T("Quality Off / Fast / Balanced / Cinematic plus key light, shadow, occlusion, gloss, rim, emission, "
                  "exposure and camera tilt.",
                  "Chất lượng Off / Fast / Balanced / Cinematic cùng đèn chính, bóng, occlusion, độ bóng, viền, "
                  "phát sáng, phơi sáng và nghiêng camera."),
                T("On the GPU stage those sliders go straight into HLSL and are re-applied every frame; the quality "
                  "selector shapes the software renderer, which bakes the keyboard once and repaints a small tile "
                  "per sounding key to hold 60 fps.",
                  "Trên sân khấu GPU, các thanh trượt đó đi thẳng vào HLSL và được áp lại ở mỗi khung hình; bộ chọn "
                  "chất lượng định hình bộ dựng hình phần mềm, nơi bàn phím bake một lần rồi chỉ vẽ lại một tile nhỏ "
                  "cho mỗi phím kêu để giữ 60 fps."),
                T("Keys of sounding MIDI notes light up as well, not only the keys a player presses.",
                  "Phím của nốt MIDI đang phát cũng sáng, chứ không chỉ phím người chơi nhấn."),
            ],
            actions=[{"label": T("Keyboard page of the dock", "Trang Keyboard của bàn cài đặt"),
                      "href": "features/design.html#dock", "kind": "btn-ghost", "icon": "sliders"}],
            media=framed(doc, "stage-gpu",
                         T("Neon Violet, the default stage, with a held chord",
                           "Neon Violet, sân khấu mặc định, với một hợp âm đang giữ"),
                         T("Neon Violet, the default look: hold effects join the keys of a chord that is being held.",
                           "Neon Violet, diện mạo mặc định: hiệu ứng giữ phím nối các phím của một hợp âm đang giữ."),
                         badge=T("GPU stage · Neon Violet", "Sân khấu GPU · Neon Violet")),
        ),

        split(
            id="backgrounds",
            eyebrow=T("Backgrounds & hit line", "Nền & đường chạm"),
            title=T("A backdrop that can stay out of the way, or take part",
                    "Phông nền có thể đứng ngoài, hoặc tham gia vào bản nhạc"),
            ticks=[
                T("Solid colour, your own picture (PNG, JPEG, BMP, GIF, TIFF) with a 0–100 dim so the notes stay "
                  "readable, or pure green for keying.",
                  "Màu đặc, ảnh của bạn (PNG, JPEG, BMP, GIF, TIFF) kèm mức làm tối 0–100 để nốt vẫn đọc được, "
                  "hoặc xanh lá thuần để key."),
                T("Six GPU shader backgrounds — Aurora, Nebula, Prism, Ember Haze, Ocean Flow and Retro Grid — each "
                  "with intensity, speed and base colour.",
                  "Sáu nền shader GPU — Aurora, Nebula, Prism, Ember Haze, Ocean Flow và Retro Grid — mỗi nền có "
                  "cường độ, tốc độ và màu gốc."),
                T("Six hit-line motion styles — Pulse, Sweep, Twin Comets, Spectrum, Electric Arc and Ripple — with "
                  "their own intensity and speed sliders beside the halo colour.",
                  "Sáu kiểu chuyển động đường chạm — Pulse, Sweep, Twin Comets, Spectrum, Electric Arc và Ripple — "
                  "có thanh chỉnh cường độ và tốc độ riêng bên cạnh màu halo."),
                T("Aura gradient, stars with shooting stars, guide lanes, vignette, horizon glow and light beams, "
                  "plus halo colour and line.",
                  "Aura gradient, sao kèm sao băng, guide lanes, vignette, horizon glow và tia sáng, cùng màu và "
                  "đường halo."),
                T("Four independent ambient layers — Energy, Nature, Light and Cosmic — with spotlights inside Light; "
                  "all off by default so the stage stays clean.",
                  "Bốn lớp ambient độc lập — Energy, Nature, Light và Cosmic — riêng lớp Light có thêm đèn sân khấu; "
                  "mặc định tắt hết để sân khấu sạch."),
            ],
            media=framed(doc, "background-image",
                         T("A user-chosen picture behind the keys", "Ảnh nền do người dùng chọn sau bàn phím"),
                         T("Your own picture behind the keys: centre-cropped to fill the frame without stretching, "
                           "dimmed 30/100 by default so the notes stay readable.",
                           "Ảnh của bạn sau bàn phím: cắt giữa để phủ kín khung mà không méo tỉ lệ, mặc định làm tối "
                           "30/100 để nốt vẫn đọc được."),
                         badge=T("Background image", "Ảnh nền")),
        ),

        chipcloud(
            id="gpu-only",
            eyebrow=T("Only on the GPU stage", "Chỉ có trên sân khấu GPU"),
            title=T("Six things the software renderer cannot do", "Sáu thứ bộ dựng hình phần mềm không làm được"),
            items=[
                (T("Note shimmer — a band of light drifting down the body of a note, carrying the note's colour",
                   "Note shimmer — dải sáng trôi dọc thân nốt, mang theo màu của nốt"), "gold"),
                (T("Landing glow — light gathering on the key a note is about to touch, beautiful and useful for practice",
                   "Landing glow — ánh sáng tụ lại trên phím mà nốt sắp chạm, vừa đẹp vừa hữu ích khi luyện tập"), "gold"),
                (T("Halo light pulses — three bright heads running along the hit line in the Pulse style",
                   "Halo light pulses — ba đầu sáng chạy dọc đường chạm ở kiểu Pulse"), "ivory"),
                (T("Shooting stars crossing the star field behind the notes",
                   "Sao băng lướt qua nền sao phía sau các nốt"), "ivory"),
                (T("Spotlights — three soft stage lights swaying with the music",
                   "Đèn sân khấu — ba luồng đèn mềm lảo đảo theo nhạc"), "ivory"),
                (T("Hold-stream particles in the family of the burst you chose: embers, water splash, fireworks, "
                   "confetti or dust",
                   "Luồng hạt khi giữ phím theo đúng họ burst bạn chọn: than hồng, nước bắn, pháo hoa, confetti "
                   "hoặc bụi"), "copper"),
                (T("Particle physics decoupled from the music clock, so slowing the tempo never slows the sparks",
                   "Tốc độ vật lý của hạt tách khỏi đồng hồ nhạc, nên giảm tempo không làm tia lửa chậm lại"), "copper"),
            ],
        ),

        callout(
            style="tip",
            icon="gauge",
            title=T("Motion, timing and the layers that stay vector",
                    "Chuyển động, đồng hồ và những lớp vẫn là vector"),
            body=[
                T("Every animation — falling notes, petals, the backdrop, panels moving — runs on one vsync clock "
                  "(FrameClock), so nothing judders and no frame is drawn twice; the clock lets go when the stage is "
                  "at rest. A motion level of Off, Calm or Full applies to the whole interface and honours the "
                  "reduce-animation setting of Windows.",
                  "Mọi animation — nốt rơi, cánh hoa, nền, chuyển panel — chạy trên cùng một đồng hồ vsync "
                  "(FrameClock), nên không rung và không vẽ thừa khung hình; đồng hồ tự nhả khi sân khấu đứng yên. "
                  "Mức chuyển động Off, Calm hoặc Full áp dụng cho toàn giao diện và tôn trọng thiết lập giảm "
                  "animation của Windows."),
                T("The staff layer, the hand marker, the camera picture, the watermark and the key counter / FPS "
                  "readout stay WPF vector layers composited over the GPU frame — sharp at any resolution.",
                  "Khuông nhạc, điểm đánh dấu bàn tay, hình camera, watermark và bộ đếm phím / FPS vẫn là các lớp "
                  "vector WPF phủ lên khung GPU — sắc nét ở mọi độ phân giải."),
            ],
        ),

        callout(
            style="warn",
            icon="alert",
            title=T("What the stage does not do yet", "Sân khấu chưa làm được gì"),
            body=[
                T("There is no particle compute shader, no depth of field, no velocity-buffer motion blur and no "
                  "camera keyframing. A 3D perspective camera is not supported either: the stage is a flat piano "
                  "roll with slight parallax.",
                  "Chưa có particle compute shader, chưa có độ sâu trường ảnh, chưa có motion blur theo velocity "
                  "buffer và chưa keyframe camera được. Góc nhìn phối cảnh 3D cũng chưa hỗ trợ: sân khấu là "
                  "piano roll phẳng với parallax nhẹ."),
            ],
        ),

        specdl(
            id="settings",
            eyebrow=T("Where these settings live", "Những cài đặt này nằm ở đâu"),
            title=E("General → GRAPHICS ENGINE"),
            items=[
                (T("GPU frame rate", "Tốc độ khung hình GPU"),
                 T("60, 120, 144, 240 FPS or Unlimited — 144 by default.",
                   "60, 120, 144, 240 FPS hoặc không giới hạn — mặc định 144.")),
                (E("VSync"),
                 T("VSync in the GPU stage window, on by default.",
                   "VSync trong cửa sổ sân khấu GPU, mặc định bật.")),
                (T("Status line", "Dòng trạng thái"),
                 T("Names the adapter in use and how long the shaders took to compile — or says why the software "
                   "renderer took over.",
                   "Ghi rõ adapter đang dùng và thời gian biên dịch shader — hoặc nói vì sao phải chuyển sang "
                   "bộ dựng hình phần mềm.")),
                (T("Belongs to the machine", "Thuộc về máy"),
                 T("Applying a preset never changes these; a settings file that names the old Software engine is "
                   "moved to the GPU when it loads.",
                   "Áp preset không bao giờ đổi những mục này; tệp cài đặt cũ ghi engine Software sẽ được chuyển "
                   "sang GPU khi nạp.")),
            ],
        ),

        slider(
            id="pictures",
            variant="spotlight", autoplay=True, interval=6000,
            label=T("The GPU stage: four looks", "Sân khấu GPU: bốn diện mạo"),
            eyebrow=T("Pictures", "Hình ảnh"),
            title=T("The same engine, four looks", "Cùng một engine, bốn diện mạo"),
            sub=T("The pictures change by themselves; use the arrows to choose, or click a picture to open it full size. "
                  "Every frame is rendered by Keyflow in CI.",
                  "Ảnh tự chuyển; dùng mũi tên để chọn, hoặc bấm vào ảnh để xem cỡ lớn. "
                  "Mọi khung hình đều do Keyflow render trong CI."),
            slides=[
                {"shot": "stage-gpu", "cap": T("Neon Violet — the default stage", "Neon Violet — sân khấu mặc định")},
                {"shot": "stage-gpu-galaxy", "cap": T("Galaxy Voyage — rainbow trails and a cosmic layer",
                                                      "Galaxy Voyage — vệt cầu vồng và lớp nền vũ trụ")},
                {"shot": "stage-gpu-storm", "cap": T("Electric Storm — speed lines and arcs between held keys",
                                                     "Electric Storm — vệt tốc độ và tia điện giữa các phím giữ")},
                {"shot": "stage-live", "cap": T("Live play — only the notes you play, with the transport bar below",
                                                "Chơi trực tiếp — chỉ hiện nốt bạn chơi, kèm thanh transport bên dưới")},
            ],
            actions=[{"label": T("Open the gallery", "Mở thư viện ảnh"), "href": "gallery.html",
                      "kind": "btn-ghost", "icon": "image"}],
        ),

        pagenav(prev=("index.html", "home"), next=("features/practice.html", "practice")),
        cta(
            title=T("See it move on your own machine", "Xem nó chuyển động trên máy của bạn"),
            sub=T("The GPU stage is the default from the first launch — there is nothing to switch on.",
                  "Sân khấu GPU là mặc định ngay từ lần mở đầu — không phải bật gì cả."),
            actions=[DOWNLOAD,
                     {"label": T("System requirements", "Yêu cầu hệ thống"), "href": "download.html#requirements",
                      "kind": "btn-ghost", "icon": "chip"}],
        ),
    ]
    return {
        "title": T("GPU stage & concert VFX · Keyflow", "Sân khấu GPU & hiệu ứng sân khấu · Keyflow"),
        "description": T(
            "Keyflow's stage is a Direct3D 11 engine on its own thread: 16-bit HDR, multi-level bloom, 24,000 "
            "particles, seven trail families, six shader backgrounds and an 88-key keyboard shaded in HLSL with GGX, "
            "a softbox and an ACES tonemap.",
            "Sân khấu của Keyflow là engine Direct3D 11 chạy trên luồng riêng: HDR 16-bit, bloom nhiều tầng, "
            "24.000 hạt, bảy họ vệt rơi, sáu nền shader và bàn phím 88 phím đổ bóng bằng HLSL với GGX, softbox "
            "và tonemap ACES."),
        "og_image": "previews/en/stage-gpu-galaxy.png",
        "crumb_trail": TRAIL + [("GPU stage & VFX", "features/stage.html")],
        "body": body,
    }


# ===========================================================================
# 2. Practice & scoring
# ===========================================================================
def build_practice(doc) -> dict:
    body = [
        feature_hero(
            doc,
            crumb=T("Practice & scoring", "Luyện tập & chấm điểm"),
            eyebrow=T("Practice mode", "Chế độ luyện tập"),
            title=T("Learn a piece note by note, and keep the evidence",
                    "Học một bản nhạc từng nốt một, và giữ lại bằng chứng"),
            lead=T("The score can wait for you. Keyflow grades every note, remembers every run, draws fourteen days "
                   "of progress and overlays your best take as a ghost — so practice is measured, not guessed.",
                   "Bản nhạc có thể chờ bạn. Keyflow chấm từng nốt, nhớ mọi lượt chơi, vẽ tiến bộ 14 ngày và phủ "
                   "lượt tốt nhất lên thành bóng — để việc luyện tập được đo, chứ không phải đoán."),
            chips=[
                T("4 practice modes", "4 chế độ tập"),
                T("A-B loop · tempo 50–150%", "Vòng lặp A-B · tempo 50–150%"),
                T("Automatic practice tempo", "Tempo luyện tập tự động"),
                T("14-day chart & ghost", "Biểu đồ 14 ngày & bóng luyện tập"),
            ],
            shot="practice-dock",
            alt=T("The Practice page: modes, tempo and the A-B loop",
                  "Trang Practice: chế độ tập, tempo và vòng lặp A-B"),
            cap=T("The Practice page of the dock: mode, tempo, loop points and the automatic practice tempo.",
                  "Trang Practice của bàn cài đặt: chế độ tập, tempo, điểm vòng lặp và tempo luyện tập tự động."),
            badge=T("Session · Practice", "Phiên · Luyện tập"),
        ),

        band(stats=[
            (("4", "4"), T("practice modes", "chế độ luyện tập"), 4),
            (("50–150%", "50–150%"), T("tempo range", "dải tempo"), None),
            (("14", "14"), T("days of practice chart", "ngày trên biểu đồ"), 14),
            (("256", "256"), T("graded notes kept per run", "nốt đã chấm giữ mỗi lượt"), 256),
        ]),

        grid(
            id="modes",
            eyebrow=T("Modes", "Chế độ"),
            title=T("Four ways to work through a piece", "Bốn cách đi qua một bản nhạc"),
            cards=[
                {"icon": "note", "t": T("Follow along", "Chơi theo"),
                 "d": T("The score runs at its own tempo while you play; every note is graded as it passes.",
                        "Bản nhạc chạy theo tempo của nó trong khi bạn chơi; mỗi nốt đều được chấm khi đi qua.")},
                {"icon": "clock", "t": T("Wait for my note", "Chờ nốt của tôi"),
                 "d": T("The score stops and waits: it only moves on once you play the right note.",
                        "Bản nhạc dừng lại và chờ: chỉ đi tiếp khi bạn bấm đúng nốt.")},
                {"icon": "hand", "t": T("Right hand only", "Chỉ tay phải"),
                 "d": T("Practise one hand while the other keeps playing, read straight from the MusicXML staves.",
                        "Tập riêng một tay trong khi tay kia vẫn chạy, đọc thẳng từ khuông nhạc MusicXML.")},
                {"icon": "hand", "t": T("Left hand only", "Chỉ tay trái"),
                 "d": T("The mirrored mode — the same split point feeds the per-hand colours too.",
                        "Chế độ đối xứng — cùng một điểm chia tay cũng phục vụ màu theo từng tay.")},
                {"icon": "loop", "t": T("A-B loop", "Vòng lặp A-B"),
                 "d": T("Set A and B at the playhead, clear with ×; every loop is re-scored from the start.",
                        "Đặt A và B tại playhead, xoá bằng ×; mỗi vòng lặp được chấm lại từ đầu.")},
                {"icon": "gauge", "t": T("Automatic practice tempo", "Tempo luyện tập tự động"),
                 "d": T("Off by default. Miss too many in a row and the song slows by 5% per step down to a 50% "
                        "floor; four correct notes speed it back up by 2%, never past 100%.",
                        "Mặc định tắt. Sai liên tiếp quá ngưỡng thì bài chậm dần 5% mỗi bước tới sàn 50%; "
                        "đúng liên tiếp 4 nốt thì nhanh lại 2%, không bao giờ vượt 100%.")},
            ],
        ),

        split(
            id="split-point",
            flip=True,
            eyebrow=T("Hands", "Hai bàn tay"),
            title=T("The hand split is read, not guessed", "Điểm chia tay được đọc, không phải đoán"),
            ticks=[
                T("The default split is C4 = MIDI 60 (Notes → Hand split point), shared by the per-hand colours and "
                  "the one-hand practice modes.",
                  "Mặc định điểm chia là C4 = MIDI 60 (Notes → Hand split point), dùng chung cho màu theo tay "
                  "và các chế độ tập từng tay."),
                T("With “Infer hand split from the song” on, opening a MIDI file picks the split from how its notes "
                  "spread over the keyboard: two clusters weighted by sounding time, accepted only when at least "
                  "five empty semitones separate the hands and each carries ten percent of the sounding time, then "
                  "settled at middle C inside the gap.",
                  "Khi bật “Infer hand split from the song”, mở một tệp MIDI sẽ tự chọn điểm chia theo cách nốt "
                  "trải trên bàn phím: gom hai cụm theo thời lượng vang, chỉ nhận khi giữa hai tay có ít nhất "
                  "năm nửa cung trống và mỗi tay chiếm mười phần trăm thời lượng vang, rồi ưu tiên nốt C giữa "
                  "trong khoảng trống đó."),
                T("The inferred value is remembered for that song, so reopening it never re-measures; a one-hand song "
                  "or two overlapping hands keep the split you chose.",
                  "Giá trị suy ra được nhớ riêng cho bài đó, nên mở lại không đo lại; bài chỉ một tay hoặc hai tay "
                  "chồng lấn thì giữ nguyên điểm bạn chọn."),
                T("For MusicXML the split comes straight from the staves — staff 1 is the right hand, staff 2 the "
                  "left, or one part per hand — and is saved with the file.",
                  "Với MusicXML, điểm chia đọc thẳng từ khuông nhạc — khuông 1 là tay phải, khuông 2 là tay trái, "
                  "hoặc mỗi tay một part — và được lưu theo tệp."),
            ],
            media=framed(doc, "play-dialog",
                         T("The Play dialog: choose a score, a hand preset and the session controls",
                           "Hộp thoại Play: chọn bản nhạc, preset cho từng tay và các điều khiển phiên"),
                         T("The Play dialog: score chooser, per-hand preset cards, quick adjustments and the "
                           "recent/library lists.",
                           "Hộp thoại Play: bộ chọn bài, thẻ preset cho từng tay, chỉnh nhanh và danh sách "
                           "gần đây / thư viện."),
                         badge=T("Perform & Play", "Biểu diễn & Phát")),
        ),

        split(
            id="sheet",
            eyebrow=T("Sheet music layer", "Lớp khuông nhạc"),
            title=T("Real notation drawn over the piano roll", "Ký âm thật vẽ trên piano roll"),
            body=[T("Switch Sheet music on in the LAYERS card and a double staff runs above the keyboard, following "
                    "the playhead. It is a reading layer built from the song's own notes and beat grid — not an "
                    "imported engraving — and everything it needs is worked out once and cached.",
                    "Bật Sheet music ở thẻ LAYERS và một khuông đôi sẽ chạy phía trên bàn phím, đi theo playhead. "
                    "Đây là lớp đọc nốt dựng từ chính nốt và lưới phách của bài — không phải bản khắc nhạc nhập vào — "
                    "và mọi thứ nó cần đều được tính một lần rồi giữ lại.")],
            ticks=[
                T("The key signature is inferred from the song itself (a Krumhansl–Kessler correlation over how long "
                  "each pitch sounds), so F major writes a B♭ on the B line rather than an A♯ on the A line; a song "
                  "that matches no key is written in C major.",
                  "Hoá biểu được suy ra từ chính bài (tương quan Krumhansl–Kessler trên thời lượng vang của từng "
                  "cao độ), nên F major viết B♭ trên dòng B chứ không phải A♯ trên dòng A; bài không khớp tông nào "
                  "thì viết theo C major."),
                T("Accidentals appear only where the bar really needs them: notes already in the key signature stay "
                  "plain, a sharp or flat holds to the end of its own bar and staff, and a natural sign restores.",
                  "Dấu hoá chỉ hiện khi ô nhịp thật sự cần: nốt đã có trong hoá biểu thì để trơn, dấu thăng/giáng "
                  "giữ đến hết ô nhịp của chính khuông đó, và dấu hoàn ♮ lấy lại nốt tự nhiên."),
                T("Short notes are beamed by the song's own beat grid with single, double and triple flags; a note in "
                  "between breaks the beam, and rests never join one.",
                  "Nốt ngắn được nối đuôi theo đúng lưới phách của bài, với cờ móc đơn/đôi/ba; nốt chen giữa làm "
                  "đứt đuôi nối, và dấu nghỉ không bao giờ vào đuôi nối."),
                T("A chord becomes one column of note heads sharing a single stem, and the silent hand gets proper "
                  "rests — one rest for a continuous silence, a whole-bar rest for each fully silent bar.",
                  "Hợp âm được ghép thành một cột nốt chung một đuôi, còn tay đang im lặng có dấu nghỉ đúng cách — "
                  "khoảng lặng liền mạch chỉ một dấu, mỗi ô im hoàn toàn một dấu nghỉ tròn."),
                T("Notes carried across a bar line are tied, the tie curves away from the stem side, and the "
                  "accidental travels with it; a line changing hands gets a curve across the gap between the staves.",
                  "Nốt vắt qua vạch nhịp được nối bằng dấu luyến, đường cong vẽ về phía đuôi quay đi và dấu hoá đi "
                  "theo dấu luyến; chỗ dòng nhạc đổi tay có một đường cong vắt qua khoảng giữa hai khuông."),
                T("The whole plan — accidentals, beams, rests, ties, chords — is kept between frames and rebuilt only "
                  "when the song, the beat grid, the hand split or the key changes.",
                  "Toàn bộ phần tính trước — dấu hoá, đuôi nối, dấu nghỉ, dấu luyến, hợp âm — được giữ giữa các "
                  "khung hình và chỉ tính lại khi đổi bài, đổi lưới phách, đổi điểm chia tay hay đổi tông."),
            ],
            actions=[{"label": T("Import formats", "Định dạng nhập bài"),
                      "href": "features/sound.html#import", "kind": "btn-ghost", "icon": "file"}],
            media=framed(doc, "stage-live",
                         T("The live stage, where the staff layer is drawn",
                           "Sân khấu live, nơi lớp khuông nhạc được vẽ"),
                         T("The live stage: the staff layer is composited over the same frame, above the piano roll.",
                           "Sân khấu live: lớp khuông nhạc được phủ lên cùng khung hình, phía trên piano roll."),
                         badge=T("Live stage", "Sân khấu live")),
        ),

        table(
            id="scoring",
            eyebrow=T("Scoring & history", "Chấm điểm & lịch sử"),
            title=T("What gets measured, and where it is kept", "Những gì được đo, và lưu ở đâu"),
            head=[T("Where", "Ở đâu"), T("What you get", "Bạn nhận được gì")],
            rows=[
                [T("Under the stage", "Ngay dưới sân khấu"),
                 T("ACCURACY, SCORE and STREAK update live, with hit/miss feedback at the moment the note passes.",
                   "ACCURACY, SCORE và STREAK cập nhật trực tiếp, kèm phản hồi đúng/sai ngay thời điểm nốt đi qua.")],
                [T("History page", "Trang History"),
                 T("Every run of the open song — when, accuracy, hits and misses, longest streak — plus the best "
                   "take of that song, EXPORT HTML for a report and CLEAR HISTORY.",
                   "Từng lượt chơi của bài đang mở — thời điểm, độ chính xác, nốt đúng/sai, chuỗi dài nhất — cùng "
                   "lượt tốt nhất của bài đó, nút EXPORT HTML để xuất báo cáo và CLEAR HISTORY.")],
                [T("Practice chart", "Biểu đồ luyện tập"),
                 T("One column per day for the last fourteen days, height set by that day's accuracy, days without "
                   "practice still on the axis, and the run count and window average printed below.",
                   "Mỗi ngày một cột trong 14 ngày gần nhất, cột cao theo độ chính xác của ngày đó, ngày không "
                   "luyện vẫn nằm trên trục, dòng dưới in số lượt và trung bình của cả cửa sổ.")],
                [T("Ghost of this song", "Bóng của bài đang mở"),
                 T("Each dot is a graded note — across by its place in the song, up by its pitch, cyan for a hit and "
                  "red for a miss. The best take and the latest take share one axis, so they can be compared; a song "
                  "never played prints the reason instead of an empty frame.",
                   "Mỗi chấm là một nốt đã chấm điểm — ngang theo vị trí trong bài, dọc theo cao độ, xanh là trúng "
                   "và đỏ là trượt. Lượt tốt nhất và lượt mới nhất dùng chung trục nên so sánh được; bài chưa chơi "
                   "lần nào thì in lý do thay vì một khung rỗng.")],
                [T("On disk", "Trên đĩa"),
                 T("One JSON line per run in history/practice.jsonl inside the settings folder, newest first with a "
                  "cap, and up to 256 graded notes per run for the ghost; a corrupt line is skipped, not fatal.",
                   "Mỗi lượt chơi một dòng JSON trong history/practice.jsonl của thư mục cài đặt, mới nhất trước "
                   "và có trần, cùng tối đa 256 nốt đã chấm mỗi lượt cho phần bóng; dòng hỏng bị bỏ qua chứ không "
                   "gây lỗi.")],
            ],
        ),

        steps(
            id="session",
            cols=4,
            eyebrow=T("A session", "Một buổi tập"),
            title=T("How a practice run goes", "Một lượt luyện tập diễn ra thế nào"),
            items=[
                {"t": T("Open the song", "Mở bài"),
                 "d": T("Play in the header → a MIDI file or a MusicXML score, or pick one from RECENT / LIBRARY "
                        "with its saved values.",
                        "Play trên header → tệp MIDI hoặc bản MusicXML, hoặc chọn từ RECENT / LIBRARY kèm các "
                        "giá trị đã lưu.")},
                {"t": T("Choose the mode", "Chọn chế độ tập"),
                 "d": T("Follow along, Wait for my note, or one hand only; set the tempo and, if you want it, the "
                        "automatic practice tempo.",
                        "Chơi theo, Chờ nốt của tôi, hoặc chỉ một tay; đặt tempo và bật tempo luyện tập tự động "
                        "nếu muốn.")},
                {"t": T("Loop the hard bar", "Lặp chỗ khó"),
                 "d": T("Set A and B on the timeline, slow to 50%, and let each loop be scored from the start.",
                        "Đặt A và B trên thanh thời gian, giảm còn 50%, và mỗi vòng lặp được chấm lại từ đầu.")},
                {"t": T("Read the ghost", "Đọc bóng luyện tập"),
                 "d": T("Stop the transport and the run is written down; History shows the chart and your best take "
                        "overlaid on the latest.",
                        "Dừng transport là lượt chơi được ghi lại; History hiện biểu đồ và lượt tốt nhất phủ lên "
                        "lượt mới nhất.")},
            ],
            note=T("Seeking, changing the mode or a track, and setting an A-B loop never count the skipped notes as "
                   "misses.",
                   "Tua bài, đổi chế độ hoặc đổi track, và đặt vòng lặp A-B đều không tính các nốt bị bỏ qua "
                   "là miss."),
        ),

        callout(
            style="gold",
            icon="info",
            title=T("Honest about the staff layer", "Nói thẳng về lớp khuông nhạc"),
            body=[T("It is a reading layer, not a full engraving: each new staff carries one voice, several voices on "
                    "one staff are not drawn yet, and slurs or articulations are not read from the score itself. "
                    "Notes are placed by pitch, the hand split decides the staff, and a note never moves down when "
                    "its pitch goes up.",
                    "Đây là lớp đọc nốt, chưa phải bản khắc nhạc đầy đủ: mỗi khuông mới có một bè, chưa vẽ nhiều bè "
                    "trên cùng một khuông, và dấu luyến hay articulation chưa được đọc từ chính bản nhạc. "
                    "Nốt được đặt theo cao độ, điểm chia tay quyết định khuông, và nốt cao hơn không bao giờ bị "
                    "viết thấp hơn.")],
        ),

        pagenav(prev=("features/stage.html", "stage"), next=("features/sound.html", "sound")),
        cta(
            title=T("Practise with the stage on", "Luyện tập cùng sân khấu đang sáng"),
            sub=T("Every practice feature is in the same free download as the concert visuals.",
                  "Mọi tính năng luyện tập đều nằm trong cùng một bản tải miễn phí với phần hình ảnh hoà nhạc."),
            actions=[DOWNLOAD,
                     {"label": T("Sound & MIDI", "Âm thanh & MIDI"), "href": "features/sound.html",
                      "kind": "btn-ghost", "icon": "arrow"}],
        ),
    ]
    return {
        "title": T("Practice, scoring & practice history · Keyflow",
                   "Luyện tập, chấm điểm & lịch sử luyện tập · Keyflow"),
        "description": T(
            "Keyflow's practice mode waits for the right note, isolates one hand, loops A-B, slows to 50% and adapts "
            "the tempo when you miss. Accuracy, streaks, a fourteen-day chart and a ghost of your best take are kept "
            "for every run.",
            "Chế độ luyện tập của Keyflow chờ bạn bấm đúng nốt, tập riêng một tay, lặp A-B, giảm tốc còn 50% và tự "
            "điều chỉnh tempo khi bạn sai. Độ chính xác, chuỗi đúng, biểu đồ 14 ngày và bóng của lượt chơi tốt nhất "
            "được giữ lại cho từng lượt."),
        "og_image": "previews/en/practice-dock.png",
        "crumb_trail": TRAIL + [("Practice & scoring", "features/practice.html")],
        "body": body,
    }


# ===========================================================================
# 3. Sound & MIDI
# ===========================================================================
def build_sound(doc) -> dict:
    body = [
        feature_hero(
            doc,
            crumb=T("Sound & MIDI", "Âm thanh & MIDI"),
            eyebrow=T("Audio, MIDI & scores", "Âm thanh, MIDI & bản nhạc"),
            title=T("A concert grand in the box, and your own if you prefer",
                    "Có sẵn một cây grand hoà nhạc, và của riêng bạn nếu muốn"),
            lead=T("Keyflow bundles a Yamaha grand SoundFont, renders stereo 44.1 kHz through the Windows audio "
                   "device, answers all three pedals, plays through your MIDI keyboard or the computer keys, and "
                   "reads MIDI and MusicXML scores properly — tempo maps, meter changes, per-track colours and all.",
                   "Keyflow kèm sẵn SoundFont grand Yamaha, phát stereo 44.1 kHz qua thiết bị âm thanh của Windows, "
                   "nhận đủ ba pedal, chơi bằng đàn MIDI hoặc bàn phím máy tính, và đọc tử tế cả bản nhạc MIDI lẫn "
                   "MusicXML — tempo map, đổi nhịp, màu theo từng track, đủ cả."),
            chips=[
                E("YDP Grand Piano · FreePats"), E("44.1 kHz stereo"),
                T("Three pedals (CC 64 / 66 / 67)", "Ba pedal (CC 64 / 66 / 67)"),
                E("MIDI in & out"), E("MIDI 0/1/2 · MusicXML"),
            ],
            shot="main-menu",
            alt=T("The Concert Grand start menu", "Menu khởi động Concert Grand"),
            cap=T("The start menu: “Audio & MIDI Hardware Setup” opens the sound pages, “Perform & Play” the session "
                  "dialog.",
                  "Menu khởi động: “Audio & MIDI Hardware Setup” mở các trang âm thanh, “Perform & Play” mở hộp "
                  "thoại phiên."),
            badge=T("Concert Grand menu", "Menu Concert Grand"),
        ),

        band(stats=[
            (("44.1 kHz", "44.1 kHz"), T("stereo render through waveOut", "stereo phát qua waveOut"), None),
            (("3", "3"), T("MIDI pedals supported", "pedal MIDI được hỗ trợ"), 3),
            (("113 MiB", "113 MiB"), T("bundled SoundFont", "SoundFont đi kèm"), None),
            (("500", "500"), T("songs indexed from one folder", "bài được lập chỉ mục từ một thư mục"), 500),
        ]),

        split(
            id="soundfont",
            eyebrow=T("The bundled piano", "Cây đàn đi kèm"),
            title=T("A Yamaha Disklavier Pro multisample, loaded for you",
                    "Bộ multisample Yamaha Disklavier Pro, nạp sẵn cho bạn"),
            ticks=[
                T("Keyflow ships the YDP Grand Piano SF2 from FreePats, built from a Yamaha Disklavier Pro "
                  "multisample, with the acoustic-grand preset already selected.",
                  "Keyflow đi kèm YDP Grand Piano SF2 của FreePats, dựng từ multisample Yamaha Disklavier Pro, "
                  "với preset grand acoustic được chọn sẵn."),
                T("It loads automatically when the app opens — a few seconds, and the label on the Audio page tells "
                  "you when it is ready.",
                  "SoundFont tự nạp khi mở ứng dụng — mất vài giây, và nhãn trên trang Audio báo khi xong."),
                T("Load any uncompressed .sf2 of your own from Settings → Audio → LOAD SOUNDFONT, then pick a "
                  "bank/program preset from the list below it. Polyphony is handled for you.",
                  "Mở Settings → Audio → LOAD SOUNDFONT để nạp bất kỳ tệp .sf2 không nén nào của bạn, rồi chọn "
                  "preset bank/program trong danh sách bên dưới. Đa âm được xử lý sẵn."),
                T("Hall reverb runs in real time in stereo, is on by default, has its own bypass button and keeps "
                  "ringing after you release a key.",
                  "Hall reverb chạy thời gian thực ở stereo, bật mặc định, có nút bypass riêng và vẫn vang sau khi "
                  "bạn nhả phím."),
            ],
            media=framed(doc, "design-dock",
                         T("The design dock, where every sound and stage setting lives",
                           "Bàn thiết kế, nơi chứa mọi cài đặt âm thanh và sân khấu"),
                         T("The dock holds the Audio and MIDI pages next to the stage pages — one search box covers "
                           "all of them.",
                           "Bàn cài đặt đặt trang Audio và MIDI cạnh các trang sân khấu — một ô tìm kiếm bao hết."),
                         badge=T("Design dock", "Bàn thiết kế")),
        ),

        callout(
            style="warn",
            icon="alert",
            title=T("What the built-in synthesizer does not do", "Bộ tổng hợp tích hợp chưa làm được gì"),
            body=[T(".sf3 is not supported, and some advanced SF2 parts — modulators, instrument filters and the "
                    "reverb/chorus effects — are not fully reproduced, so the sound can differ from a dedicated "
                    "SoundFont synthesizer depending on the file. The bundled SoundFont is about 113 MiB; its "
                    "authors, source and CC BY 3.0 licence are credited in Assets/ATTRIBUTION.txt inside every "
                    "package.",
                    "Định dạng .sf3 chưa được hỗ trợ, và một số phần SF2 nâng cao — modulators, bộ lọc nhạc cụ và "
                    "hiệu ứng reverb/chorus — chưa được tái tạo đầy đủ, nên âm thanh có thể khác một bộ tổng hợp "
                    "SoundFont chuyên dụng tùy theo tệp. SoundFont đi kèm nặng khoảng 113 MiB; tác giả, nguồn và "
                    "giấy phép CC BY 3.0 được ghi công trong Assets/ATTRIBUTION.txt nằm trong mỗi gói.")],
        ),

        grid(
            id="pedals",
            eyebrow=T("Pedals & input", "Pedal & đầu vào"),
            title=T("Three pedals, four ways to play a note", "Ba pedal, bốn cách tạo ra một nốt"),
            cards=[
                {"icon": "wave", "t": E("Sustain · CC 64"),
                 "d": T("The damper pedal: the sound keeps going after you release the key.",
                        "Pedal damper: tiếng đàn vẫn giữ sau khi bạn nhả phím.")},
                {"icon": "wave", "t": E("Sostenuto · CC 66"),
                 "d": T("Holds only the notes that were already sounding when the pedal went down.",
                        "Chỉ giữ những nốt đang kêu tại thời điểm pedal được nhấn xuống.")},
                {"icon": "wave", "t": E("Una corda · CC 67"),
                 "d": T("The soft pedal: lower gain and a gentler timbre.",
                        "Pedal mềm: giảm gain và làm dịu âm sắc.")},
                {"icon": "keys", "t": T("Computer keyboard", "Bàn phím máy tính"),
                 "d": T("A W S E D F T G Y H U J K play one octave from middle C; hold a key to sustain, release "
                        "to send Note Off.",
                        "A W S E D F T G Y H U J K chơi một quãng tám từ nốt C giữa; nhấn giữ để duy trì nốt, "
                        "thả ra để gửi Note Off.")},
                {"icon": "piano", "t": T("On-screen piano", "Piano trên màn hình"),
                 "d": T("Click or drag over the keys with the full colour, spark and flame response.",
                        "Click hoặc kéo trên phím với đầy đủ phản hồi màu, tia lửa và lửa.")},
                {"icon": "plug", "t": T("MIDI instrument", "Đàn MIDI"),
                 "d": T("Velocity, Note On/Off and all three pedals enter the same feedback pipeline; the badge "
                        "above the keyboard reads MIDI IN · C4 when a note arrives.",
                        "Velocity, Note On/Off và cả ba pedal đi vào cùng luồng phản hồi; nhãn phía trên bàn phím "
                        "hiện MIDI IN · C4 khi có nốt vào.")},
            ],
        ),

        table(
            id="midi",
            eyebrow=T("MIDI devices", "Thiết bị MIDI"),
            title=T("Plug it in before you launch, or refresh later",
                    "Cắm đàn trước khi mở app, hoặc làm mới sau"),
            head=[T("Situation", "Tình huống"), T("What Keyflow does", "Keyflow làm gì")],
            rows=[
                [T("Keyboard plugged in at launch", "Cắm đàn trước khi mở ứng dụng"),
                 T("The first MIDI input found is connected automatically.",
                   "Tự động kết nối ngõ vào MIDI đầu tiên tìm thấy.")],
                [T("Plugged in later", "Cắm đàn sau"),
                 T("Settings → MIDI → Refresh devices selects and connects the new instrument; the device you chose "
                   "is kept after a refresh.",
                   "Settings → MIDI → Refresh devices sẽ chọn và kết nối đàn mới; thiết bị bạn đã chọn được giữ "
                   "sau khi làm mới danh sách.")],
                [T("Playing through an external synth", "Phát qua synth ngoài"),
                 T("WinMM MIDI output sends Note On/Off to the device you pick — an extra audio path beside the "
                   "internal SoundFont.",
                   "Ngõ ra WinMM MIDI gửi Note On/Off tới thiết bị bạn chọn — một đường âm thanh bổ sung cạnh "
                   "SoundFont nội bộ.")],
                [T("Keeping time", "Giữ nhịp"),
                 T("A metronome that follows the tempo map and accents the first beat of each bar.",
                   "Metronome đi theo tempo map và nhấn mạnh phách đầu của mỗi ô nhịp.")],
                [T("Working with tracks", "Làm việc với track"),
                 T("The track list shows names, and each track can be soloed, muted or recoloured.",
                   "Danh sách track hiện tên, và mỗi track có thể solo, mute hoặc đổi màu.")],
            ],
        ),

        split(
            id="import",
            flip=True,
            eyebrow=T("Importing scores", "Nhập bản nhạc"),
            title=T("MIDI and MusicXML, read the way they were written",
                    "MIDI và MusicXML, đọc đúng như cách chúng được viết"),
            ticks=[
                T("MIDI formats 0, 1 and 2 — format 2 is a set of independent sequences, so they play one after "
                  "another.",
                  "MIDI định dạng 0, 1 và 2 — định dạng 2 là các chuỗi độc lập nên được chạy lần lượt, hết chuỗi "
                  "này tới chuỗi kia."),
                T("Both time divisions: PPQ, and SMPTE where ticks are absolute time, so the tempo only changes the "
                  "metronome's speed and never moves a note.",
                  "Cả hai kiểu độ chia: PPQ, và SMPTE nơi tick là thời gian tuyệt đối nên tempo chỉ đổi nhịp của "
                  "metronome chứ không dịch nốt."),
                T("Tempo maps, meter, track names, note durations and velocities are read; drum channel 10 is "
                  "ignored; seek, tempo and A-B loop work on top of all of it.",
                  "Tempo map, nhịp, tên track, thời lượng và velocity của nốt đều được đọc; kênh trống 10 bị bỏ "
                  "qua; tua, đổi tempo và vòng lặp A-B hoạt động trên toàn bộ."),
                T("MusicXML in .musicxml, .xml and compressed .mxl (read through META-INF/container.xml): "
                  "instruments, beats per bar, tempo maps, meter changes mid-song, chords, backup/forward and part "
                  "names.",
                  "MusicXML ở dạng .musicxml, .xml và .mxl nén (đọc qua META-INF/container.xml): nhạc cụ, số phách "
                  "trong ô nhịp, tempo map, nhịp đổi giữa bài, hợp âm, backup/forward và tên bè."),
                T("Broken files are rejected with a reason instead of half-loading, and a MIDI file with an unknown "
                  "format or an unusable division says so.",
                  "Tệp hỏng bị từ chối kèm lý do chứ không nạp nửa vời, và tệp MIDI có định dạng lạ hay độ chia "
                  "không dùng được sẽ được báo rõ."),
            ],
            actions=[{"label": T("The staff layer it feeds", "Lớp khuông nhạc mà nó nuôi"),
                      "href": "features/practice.html#sheet", "kind": "btn-ghost", "icon": "book"}],
            media=framed(doc, "play-dialog",
                         T("The Play dialog with a score loaded", "Hộp thoại Play khi đã nạp một bản nhạc"),
                         T("The Play dialog: MIDI and MusicXML files, per-hand presets, recent songs and the folder "
                           "library.",
                           "Hộp thoại Play: tệp MIDI và MusicXML, preset cho từng tay, bài gần đây và thư viện "
                           "theo thư mục."),
                         badge=T("Choose a score", "Chọn bản nhạc")),
        ),

        table(
            id="library",
            eyebrow=T("Library", "Thư viện bài"),
            title=T("Two lists: what you just played, and the folder you keep",
                    "Hai danh sách: bài vừa chơi, và thư mục bạn giữ"),
            head=[T("Part", "Phần"), T("How it works", "Cách hoạt động")],
            rows=[
                [E("RECENT"),
                 T("The twelve newest songs with their note and track counts, length, tempo and the preset they were "
                   "last played at. Click a row to reopen it with those exact values, × to forget it; the Play "
                   "dialog shows the first five.",
                   "Mười hai bài mới nhất kèm số nốt, số track, độ dài, tempo và preset dùng lần trước. Bấm một "
                   "dòng để mở lại đúng các giá trị đó, bấm × để quên; hộp thoại Play hiện năm dòng đầu.")],
                [E("LIBRARY"),
                 T("CHOOSE FOLDER indexes every MIDI file and MusicXML score under it — three levels deep, up to 500 "
                   "files — reading each one with the app's own reader to get its notes, tracks, length and tempo.",
                   "CHOOSE FOLDER lập chỉ mục mọi tệp MIDI và bản MusicXML bên trong — sâu ba tầng, tối đa 500 tệp — "
                   "mỗi tệp được đọc bằng chính reader của ứng dụng để lấy số nốt, số track, độ dài và tempo.")],
                [T("Tags & search", "Thẻ & tìm kiếm"),
                 T("Add tags with + TAG… (up to eight per song, trimmed and lower-cased) and remove them by clicking. "
                   "Search matches titles, file names and tags, and every word has to match.",
                   "Thêm thẻ bằng + TAG… (tối đa tám thẻ một bài, được cắt khoảng trắng và viết thường), bấm thẻ để "
                   "bỏ. Ô tìm kiếm khớp tiêu đề, tên tệp và thẻ, và phải đủ mọi từ.")],
                [T("Folder watcher", "Theo dõi thư mục"),
                 T("The folder is watched, so adding, editing or deleting a file updates the list by itself; RESCAN "
                  "re-reads everything but reuses the entries that did not change and keeps their tags.",
                   "Thư mục được theo dõi nên thêm, sửa hay xoá tệp là danh sách tự cập nhật; RESCAN đọc lại tất cả "
                   "nhưng dùng lại mục không đổi và giữ nguyên thẻ của chúng.")],
                [T("On disk", "Trên đĩa"),
                 T("The index lives in library-index.json and only re-reads files that changed; a corrupt index reads "
                  "as an empty library instead of an error, and the search box stays hidden until something is "
                  "indexed.",
                   "Chỉ mục nằm trong library-index.json và chỉ đọc lại tệp đã thay đổi; chỉ mục hỏng đọc thành thư "
                   "viện rỗng thay vì báo lỗi, và ô tìm kiếm không hiện khi chưa lập chỉ mục.")],
            ],
        ),

        callout(
            style="tip",
            icon="info",
            title=T("Sound and recording are wired together", "Âm thanh và ghi hình được nối với nhau"),
            body=[T("Recording taps the very PCM blocks the engine plays, and the tap is attached only while a "
                    "recording runs — so performing costs nothing extra. MP4 gets those samples as AAC inside the "
                    "file; AVI and PNG sequences get a 16-bit stereo WAV beside them. <a class=\"link-plain\" href=\"../features/recording.html\">How a take is written \u2192</a>",
                    "Việc ghi hình lấy đúng những khối PCM mà engine phát, và tap này chỉ được gắn trong lúc ghi — "
                    "nên lúc diễn bình thường không tốn gì thêm. MP4 nhận những mẫu đó dưới dạng AAC ngay trong tệp; "
                    "AVI và chuỗi PNG có một tệp WAV stereo 16-bit nằm cạnh. <a class=\"link-plain\" href=\"../features/recording.html\">Cách một bản ghi được viết ra \u2192</a>")],
        ),

        pagenav(prev=("features/practice.html", "practice"), next=("features/recording.html", "recording")),
        cta(
            title=T("Play the first note in a minute", "Bấm nốt đầu tiên trong một phút"),
            sub=T("The SoundFont loads itself, the first MIDI input connects itself, and the computer keyboard plays "
                  "right away.",
                  "SoundFont tự nạp, ngõ vào MIDI đầu tiên tự kết nối, và bàn phím máy tính chơi được ngay."),
            actions=[DOWNLOAD,
                     {"label": T("First-time setup", "Thiết lập lần đầu"), "href": "guide.html#setup",
                      "kind": "btn-ghost", "icon": "book"}],
        ),
    ]
    return {
        "title": T("Sound, MIDI & score import · Keyflow", "Âm thanh, MIDI & nhập bản nhạc · Keyflow"),
        "description": T(
            "Keyflow bundles a Yamaha grand SoundFont with hall reverb and all three pedals, plays from a MIDI "
            "keyboard, the on-screen piano or the computer keys, and reads MIDI formats 0/1/2, PPQ and SMPTE "
            "divisions and MusicXML scores — with a tagged folder library.",
            "Keyflow kèm SoundFont grand Yamaha với hall reverb và đủ ba pedal, chơi bằng đàn MIDI, piano trên màn "
            "hình hoặc bàn phím máy tính, và đọc MIDI định dạng 0/1/2, độ chia PPQ lẫn SMPTE cùng bản nhạc "
            "MusicXML — kèm thư viện theo thư mục có gắn thẻ."),
        "og_image": "previews/en/main-menu.png",
        "crumb_trail": TRAIL + [("Sound & MIDI", "features/sound.html")],
        "body": body,
    }
