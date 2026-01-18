import streamlit as st
import validators
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    TranscriptsDisabled,
    NoTranscriptFound,
    VideoUnavailable
)
from urllib.parse import urlparse, parse_qs
import re


# Page configuration
st.set_page_config(
    page_title="YouTube Transcript Viewer",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .transcript-container {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        margin-top: 20px;
    }
    .timestamp {
        color: #0066cc;
        font-weight: 600;
        font-family: monospace;
        min-width: 80px;
        display: inline-block;
    }
    .transcript-text {
        color: #333;
        line-height: 1.8;
        font-size: 16px;
    }
    .transcript-line {
        margin-bottom: 12px;
        padding: 8px;
        border-left: 3px solid #e9ecef;
        padding-left: 12px;
    }
    .transcript-line:hover {
        background-color: #e9ecef;
        border-left-color: #0066cc;
    }
    .stTextInput > div > div > input {
        font-size: 16px;
    }
    .language-badge {
        display: inline-block;
        padding: 4px 12px;
        background-color: #e7f3ff;
        color: #0066cc;
        border-radius: 12px;
        font-size: 14px;
        margin: 2px;
    }
    </style>
    """, unsafe_allow_html=True)


def extract_video_id(url):
    """
    Extract video ID from various YouTube URL formats.

    Supports:
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtu.be/VIDEO_ID
    - https://m.youtube.com/watch?v=VIDEO_ID
    - URLs with additional parameters
    """
    if not url:
        return None

    # Remove whitespace
    url = url.strip()

    # Pattern for youtu.be short URLs
    short_pattern = r'(?:https?://)?(?:www\.)?youtu\.be/([a-zA-Z0-9_-]{11})'
    match = re.match(short_pattern, url)
    if match:
        return match.group(1)

    # Pattern for standard YouTube URLs
    try:
        parsed_url = urlparse(url)

        # Check if it's a YouTube domain
        if 'youtube.com' in parsed_url.netloc or 'youtu.be' in parsed_url.netloc:
            # For youtu.be, video ID is in path
            if 'youtu.be' in parsed_url.netloc:
                return parsed_url.path[1:]

            # For youtube.com, video ID is in query parameter 'v'
            if parsed_url.query:
                query_params = parse_qs(parsed_url.query)
                if 'v' in query_params:
                    return query_params['v'][0]

        # Try to find video ID pattern anywhere in the URL
        video_id_pattern = r'[a-zA-Z0-9_-]{11}'
        matches = re.findall(video_id_pattern, url)
        if matches:
            return matches[0]

    except Exception:
        pass

    return None


def format_timestamp(seconds):
    """
    Convert seconds to HH:MM:SS or MM:SS format.
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    else:
        return f"{minutes:02d}:{secs:02d}"


@st.cache_data(show_spinner=False)
def get_transcript(video_id, languages=None):
    """
    Fetch transcript for a video in the specified language(s).
    Auto-detects Korean or English if no language specified.
    Returns tuple of (transcript_data, detected_language).
    """
    try:
        api = YouTubeTranscriptApi()
        transcript_list = api.list(video_id)

        if languages:
            # Try to find transcript in requested languages
            transcript = transcript_list.find_transcript(languages)
        else:
            # Auto-detect: try Korean first, then English
            try:
                transcript = transcript_list.find_transcript(['ko', 'en'])
            except:
                # Fallback to any available transcript
                transcript = list(transcript_list)[0]

        # Fetch the actual transcript data and return with language info
        return transcript.fetch(), transcript.language_code
    except Exception as e:
        raise e


def process_transcript_to_paragraphs(transcript_data, pause_threshold=2.0):
    """
    Process transcript into paragraphs based on pauses and sentence structure.
    """
    paragraphs = []
    current_paragraph = {'start': None, 'texts': []}
    previous_end = 0

    for entry in transcript_data:
        if hasattr(entry, 'start'):
            start = entry.start
            text = entry.text.strip()
            duration = entry.duration if hasattr(entry, 'duration') else 2.0
        else:
            start = entry.get('start', 0)
            text = entry.get('text', '').strip()
            duration = entry.get('duration', 2.0)

        current_end = start + duration
        pause = start - previous_end

        # New paragraph if: first entry, long pause, or sentence end + pause
        if current_paragraph['start'] is None:
            current_paragraph['start'] = start
            current_paragraph['texts'].append(text)
        elif pause > pause_threshold or (pause > 1.0 and current_paragraph['texts'] and
                                          current_paragraph['texts'][-1].rstrip().endswith(('.', '!', '?', '。', '！', '？'))):
            if current_paragraph['texts']:
                paragraphs.append({
                    'start': current_paragraph['start'],
                    'text': ' '.join(current_paragraph['texts'])
                })
            current_paragraph = {'start': start, 'texts': [text]}
        else:
            current_paragraph['texts'].append(text)

        previous_end = current_end

    if current_paragraph['texts']:
        paragraphs.append({
            'start': current_paragraph['start'],
            'text': ' '.join(current_paragraph['texts'])
        })

    return paragraphs


def display_transcript(transcript_data):
    """
    Display the transcript with timestamps in paragraph format.
    """
    paragraphs = process_transcript_to_paragraphs(transcript_data)

    st.markdown('<div class="transcript-container">', unsafe_allow_html=True)

    for para in paragraphs:
        timestamp = format_timestamp(para['start'])
        text = para['text']

        st.markdown(
            f'<div class="transcript-line">'
            f'<span class="timestamp">{timestamp}</span> '
            f'<span class="transcript-text">{text}</span>'
            f'</div>',
            unsafe_allow_html=True
        )

    st.markdown('</div>', unsafe_allow_html=True)


def main():
    # Header
    st.title("📝 YouTube Transcript Viewer")
    st.markdown("유튜브 영상의 한국어/영어 자막을 자동으로 가져옵니다 | Auto-detect Korean/English transcripts")

    # Initialize session state
    if 'current_url' not in st.session_state:
        st.session_state.current_url = None
    if 'transcript_data' not in st.session_state:
        st.session_state.transcript_data = None
    if 'detected_lang' not in st.session_state:
        st.session_state.detected_lang = None
    if 'video_id' not in st.session_state:
        st.session_state.video_id = None

    # URL Input
    url_input = st.text_input(
        "YouTube URL을 입력하세요 / Enter YouTube URL",
        placeholder="https://www.youtube.com/watch?v=... or https://youtu.be/...",
        help="유튜브 영상 URL을 붙여넣으세요"
    )

    # Check if URL changed - if so, reset transcript data
    if url_input and url_input != st.session_state.current_url:
        st.session_state.current_url = url_input
        st.session_state.transcript_data = None
        st.session_state.detected_lang = None
        st.session_state.video_id = None

    if url_input:
        # Validate URL
        if not validators.url(url_input) and not url_input.startswith('http'):
            url_input = 'https://' + url_input

        if not validators.url(url_input):
            st.error("❌ Please enter a valid YouTube URL")
            return

        # Check if it's a YouTube URL
        if 'youtube.com' not in url_input and 'youtu.be' not in url_input:
            st.error("❌ Please enter a valid YouTube URL (youtube.com or youtu.be)")
            return

        # Extract video ID
        video_id = extract_video_id(url_input)

        if not video_id:
            st.error("❌ Could not extract video ID from URL. Please check the URL format.")
            return

        # Display video ID for debugging
        with st.expander("ℹ️ Video Information"):
            st.code(f"Video ID: {video_id}")
            st.markdown(f"**Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v={video_id})")

        # Auto-fetch transcript when URL is entered (if not already fetched)
        if not st.session_state.transcript_data or st.session_state.video_id != video_id:
            try:
                with st.spinner("📥 Fetching transcript..."):
                    transcript, detected_lang = get_transcript(video_id)

                if transcript:
                    # Store in session state
                    st.session_state.transcript_data = transcript
                    st.session_state.detected_lang = detected_lang
                    st.session_state.video_id = video_id
                else:
                    st.warning("⚠️ No transcript content found.")

            except TranscriptsDisabled:
                st.error("❌ 이 영상은 자막이 비활성화되어 있습니다. / Transcripts are disabled for this video.")
            except NoTranscriptFound:
                st.error("❌ 한국어 또는 영어 자막을 찾을 수 없습니다. / No Korean or English transcript found.")
                st.info("💡 이 영상에 한국어나 영어 자막이 없을 수 있습니다.")
            except VideoUnavailable:
                st.error("❌ 영상을 찾을 수 없거나 비공개 영상입니다. / Video not found or is private.")
            except Exception as e:
                st.error(f"❌ 오류가 발생했습니다 / An error occurred: {str(e)}")
                st.info("네트워크 문제, 영상 제한, 또는 자막을 사용할 수 없는 경우일 수 있습니다.")

        # Display transcript if it exists in session state
        if st.session_state.transcript_data:
            transcript = st.session_state.transcript_data
            detected_lang = st.session_state.detected_lang
            video_id = st.session_state.video_id

            # Display detected language
            lang_name = "한국어 (Korean)" if detected_lang == 'ko' else "English" if detected_lang == 'en' else detected_lang
            st.success(f"✅ Transcript retrieved successfully! ({len(transcript)} entries)")
            st.info(f"🌐 Detected language: **{lang_name}**")

            # Process into paragraphs for better readability
            paragraphs = process_transcript_to_paragraphs(transcript)

            # Prepare data for export
            transcript_lines = []
            csv_rows = ["Timestamp,Text"]  # CSV header

            # TXT: Use paragraphs for readability
            for para in paragraphs:
                timestamp = format_timestamp(para['start'])
                text = para['text']
                transcript_lines.append(f"[{timestamp}] {text}")

            # CSV: Keep original granular entries
            for entry in transcript:
                if hasattr(entry, 'start'):
                    timestamp = format_timestamp(entry.start)
                    text = entry.text
                else:
                    timestamp = format_timestamp(entry['start'])
                    text = entry['text']

                csv_text = text.replace('"', '""')
                csv_rows.append(f'"{timestamp}","{csv_text}"')

            transcript_text = "\n\n".join(transcript_lines)
            csv_content = "\n".join(csv_rows)

            # Create TXT with LLM prompt
            txt_with_prompt = f"""Please analyze this YouTube video transcript and provide:
1. A brief summary (2-3 sentences) of the main topic and key points
2. The cleaned up, readable transcript below

The transcript has been automatically processed into paragraphs for better readability.

---

VIDEO TRANSCRIPT:

{transcript_text}

---

Please process the above transcript and provide your analysis."""

            # Export options at the top
            st.markdown("---")
            st.subheader("📤 Export Options")

            # Create two columns for download buttons
            col1, col2 = st.columns(2)

            with col1:
                st.download_button(
                    label="📄 Download as TXT (with LLM prompt)",
                    data=txt_with_prompt,
                    file_name=f"transcript_{video_id}_llm.txt",
                    mime="text/plain",
                    use_container_width=True
                )

            with col2:
                st.download_button(
                    label="📊 Download as CSV",
                    data=csv_content,
                    file_name=f"transcript_{video_id}.csv",
                    mime="text/csv",
                    use_container_width=True
                )

            # Copy section with text area
            st.markdown("---")
            st.subheader("📋 Copy Text")
            st.text_area(
                "Select all (Cmd+A / Ctrl+A) and copy (Cmd+C / Ctrl+C)",
                value=transcript_text,
                height=150,
                label_visibility="collapsed"
            )

            # Display transcript
            st.markdown("---")
            st.subheader("Transcript")
            display_transcript(transcript)

    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666; font-size: 14px;'>"
        "Built with Streamlit • Powered by youtube-transcript-api"
        "</div>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
