from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import List, Optional

from flask import Flask, render_template, request, url_for, redirect, abort


app = Flask(__name__)


@dataclass
class Video:
    id: str
    title: str
    channel: str
    views: int
    published: str
    duration: str
    description: str
    thumbnail_url: str
    video_url: str

    def to_template(self) -> dict:
        video_dict = asdict(self)
        video_dict["views_display"] = f"{self.views:,} views"
        return video_dict


def generate_sample_videos() -> List[Video]:
    # Using picsum.photos for placeholder thumbnails and samplelib for video links
    sample: List[Video] = [
        Video(
            id="1",
            title="Relaxing Lofi Beats to Study and Code",
            channel="Vibe Coding",
            views=1542300,
            published="2 weeks ago",
            duration="3:12:45",
            description=(
                "Kick back with a long mix of chill lofi hip-hop beats to help you focus."
            ),
            thumbnail_url="https://picsum.photos/seed/lofi/480/270",
            video_url="https://samplelib.com/lib/preview/mp4/sample-5s.mp4",
        ),
        Video(
            id="2",
            title="Build a YouTube Clone in Flask (Full Tutorial)",
            channel="CodeCraft",
            views=452100,
            published="1 month ago",
            duration="58:13",
            description=(
                "We create a mini YouTube-style UI with Flask, templates, and static assets."
            ),
            thumbnail_url="https://picsum.photos/seed/flask/480/270",
            video_url="https://samplelib.com/lib/preview/mp4/sample-10s.mp4",
        ),
        Video(
            id="3",
            title="Top 10 Python Tricks You Should Know",
            channel="PyGenius",
            views=2300400,
            published="3 months ago",
            duration="12:07",
            description=(
                "Level up your Python with these concise, powerful patterns and tips."
            ),
            thumbnail_url="https://picsum.photos/seed/python/480/270",
            video_url="https://samplelib.com/lib/preview/mp4/sample-20s.mp4",
        ),
        Video(
            id="4",
            title="Designing Beautiful CSS Grid Layouts",
            channel="FrontEnd Garden",
            views=98765,
            published="5 days ago",
            duration="23:45",
            description=(
                "A hands-on guide to crafting modern, responsive layouts with CSS Grid."
            ),
            thumbnail_url="https://picsum.photos/seed/cssgrid/480/270",
            video_url="https://samplelib.com/lib/preview/mp4/sample-30s.mp4",
        ),
        Video(
            id="5",
            title="Algorithms Visualized: Pathfinding with A*",
            channel="AlgoViz",
            views=712340,
            published="1 year ago",
            duration="16:59",
            description=(
                "We animate the A* pathfinding algorithm to build strong intuition."
            ),
            thumbnail_url="https://picsum.photos/seed/astar/480/270",
            video_url="https://samplelib.com/lib/preview/mp4/sample-15s.mp4",
        ),
    ]
    return sample


VIDEOS: List[Video] = generate_sample_videos()
VIDEO_INDEX = {v.id: v for v in VIDEOS}


@app.route("/")
def home():
    query: str = request.args.get("q", "").strip()
    if query:
        lowered = query.lower()
        filtered = [
            v.to_template()
            for v in VIDEOS
            if lowered in v.title.lower() or lowered in v.channel.lower()
        ]
    else:
        filtered = [v.to_template() for v in VIDEOS]

    return render_template(
        "index.html",
        videos=filtered,
        query=query,
    )


@app.route("/watch/<video_id>")
def watch(video_id: str):
    video: Optional[Video] = VIDEO_INDEX.get(video_id)
    if not video:
        abort(404)

    # Simple recommendation list: others except current
    recommendations = [v.to_template() for v in VIDEOS if v.id != video_id]
    return render_template(
        "watch.html",
        video=video.to_template(),
        recommendations=recommendations,
    )


if __name__ == "__main__":
    # Enable auto-reload for development
    app.run(host="127.0.0.1", port=5000, debug=True)


