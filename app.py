"""
Claude Code Issues Dashboard
Product Ops Analysis Dashboard for Take-Home Exercise
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Claude Code Issues Analysis",
    page_icon="📊",
    layout="wide"
)

# Title
st.title("📊 Claude Code Issues Analysis")
st.markdown("**Product Operations Dashboard** | GitHub Issues Backlog Analysis")
st.markdown("---")

# Load data
@st.cache_data
def load_data():
    """Load the enriched issues CSV"""
    try:
        df = pd.read_csv('Claude_Code_Github_Categorized_ Issue_Tracker.csv', header=1)
        # Convert date columns
        df['created_at'] = pd.to_datetime(df['created_at'])
        df['updated_at'] = pd.to_datetime(df['updated_at'])
        return df
    except FileNotFoundError:
        st.error("❌ Claude_Code_Github_Categorized_ Issue_Tracker.csv not found. Please run the extraction and enrichment process first.")
        return None

df = load_data()

if df is not None:

    # Date Range and Filters Section
    st.subheader("📅 Data Overview & Filters")

    # Show date range
    min_date = df['created_at'].min()
    max_date = df['created_at'].max()
    col_date1, col_date2, col_date3 = st.columns(3)

    with col_date1:
        st.metric("Data Range Start", min_date.strftime("%Y-%m-%d"))
    with col_date2:
        st.metric("Data Range End", max_date.strftime("%Y-%m-%d"))
    with col_date3:
        days_span = (max_date - min_date).days
        st.metric("Total Days", f"{days_span} days")

    # Date filter
    st.markdown("#### Filter by Date Range")
    date_col1, date_col2 = st.columns(2)

    with date_col1:
        start_date = st.date_input(
            "Start Date",
            value=min_date,
            min_value=min_date,
            max_value=max_date
        )

    with date_col2:
        end_date = st.date_input(
            "End Date",
            value=max_date,
            min_value=min_date,
            max_value=max_date
        )

    # Additional filters
    st.markdown("#### Additional Filters")
    filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)

    with filter_col1:
        category_filter = st.multiselect(
            "Category",
            options=sorted(df['Category'].unique()),
            default=[]
        )

    with filter_col2:
        priority_filter = st.multiselect(
            "Priority",
            options=['P0', 'P1', 'P2', 'P3', 'P4'],
            default=[]
        )

    with filter_col3:
        l1_filter = st.multiselect(
            "L1 Category",
            options=sorted(df['L1_Category'].dropna().unique()),
            default=[]
        )

    with filter_col4:
        l2_filter = st.multiselect(
            "L2 Category",
            options=sorted(df['L2_Category'].dropna().unique()),
            default=[]
        )

    # Apply all filters
    filtered_df = df[
        (df['created_at'].dt.date >= start_date) &
        (df['created_at'].dt.date <= end_date)
    ].copy()

    if category_filter:
        filtered_df = filtered_df[filtered_df['Category'].isin(category_filter)]
    if priority_filter:
        filtered_df = filtered_df[filtered_df['Priority'].isin(priority_filter)]
    if l1_filter:
        filtered_df = filtered_df[filtered_df['L1_Category'].isin(l1_filter)]
    if l2_filter:
        filtered_df = filtered_df[filtered_df['L2_Category'].isin(l2_filter)]

    st.markdown("---")

    # Key Metrics Row
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Issues", len(filtered_df))

    with col2:
        high_priority = len(filtered_df[filtered_df['Priority'].isin(['P0', 'P1'])])
        st.metric("P0/P1 Priority", high_priority)

    with col3:
        negative = len(filtered_df[filtered_df['Sentiment'] == 'Negative'])
        st.metric("Negative Sentiment", negative)

    with col4:
        avg_comments = filtered_df['comments_count'].mean()
        st.metric("Avg Comments", f"{avg_comments:.1f}")

    st.markdown("---")

    # Main Charts: Issues by Category Over Time & Priority Distribution Over Time
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("📂 Issues by Category Over Time")

        # Group by week and category
        filtered_df['week'] = filtered_df['created_at'].dt.to_period('W').dt.start_time
        category_timeline = filtered_df.groupby(['week', 'Category']).size().reset_index(name='count')

        fig1 = px.area(
            category_timeline,
            x='week',
            y='count',
            color='Category',
            labels={'week': 'Week', 'count': 'Number of Issues'},
            title='Issue Volume by Category'
        )
        fig1.update_layout(height=400, hovermode='x unified')
        st.plotly_chart(fig1, use_container_width=True)

        # Show total count by category
        category_totals = filtered_df['Category'].value_counts().reset_index()
        category_totals.columns = ['Category', 'Total Issues']
        st.dataframe(category_totals, use_container_width=True, hide_index=True)

    with col_right:
        st.subheader("🎯 Priority Distribution Over Time")

        # Group by week and priority
        priority_timeline = filtered_df.groupby(['week', 'Priority']).size().reset_index(name='count')

        # Custom color mapping
        priority_colors = {
            'P0': '#8B0000',  # Dark red - Critical
            'P1': '#FF4B4B',  # Red - High
            'P2': '#FFA500',  # Orange - Medium
            'P3': '#4CAF50',  # Green - Low
            'P4': '#9E9E9E'   # Gray - Won't Do
        }

        fig2 = px.area(
            priority_timeline,
            x='week',
            y='count',
            color='Priority',
            color_discrete_map=priority_colors,
            labels={'week': 'Week', 'count': 'Number of Issues'},
            title='Priority Distribution',
            category_orders={'Priority': ['P0', 'P1', 'P2', 'P3', 'P4']}
        )
        fig2.update_layout(height=400, hovermode='x unified')
        st.plotly_chart(fig2, use_container_width=True)

        # Show total count by priority
        priority_totals = filtered_df['Priority'].value_counts().reindex(['P0', 'P1', 'P2', 'P3', 'P4'], fill_value=0).reset_index()
        priority_totals.columns = ['Priority', 'Total Issues']
        st.dataframe(priority_totals, use_container_width=True, hide_index=True)

    st.markdown("---")

    # L1 and L2 Top 10 Charts
    col_l1, col_l2 = st.columns(2)

    with col_l1:
        st.subheader("🏷️ Top 10 L1 Categories")
        l1_counts = filtered_df['L1_Category'].value_counts().head(10).reset_index()
        l1_counts.columns = ['L1 Category', 'Count']

        fig3 = px.bar(
            l1_counts,
            x='Count',
            y='L1 Category',
            orientation='h',
            color='Count',
            color_continuous_scale='Blues',
            text='Count'
        )
        fig3.update_traces(textposition='outside')
        fig3.update_layout(showlegend=False, height=400, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig3, use_container_width=True)

    with col_l2:
        st.subheader("🏷️ Top 10 L2 Categories")
        # Filter out "Other" and get top 10
        l2_filtered = filtered_df[filtered_df['L2_Category'] != 'Other']
        l2_counts = l2_filtered['L2_Category'].value_counts().head(10).reset_index()
        l2_counts.columns = ['L2 Category', 'Count']

        fig4 = px.bar(
            l2_counts,
            x='Count',
            y='L2 Category',
            orientation='h',
            color='Count',
            color_continuous_scale='Greens',
            text='Count'
        )
        fig4.update_traces(textposition='outside')
        fig4.update_layout(showlegend=False, height=400, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown("---")

    # Sentiment Analysis Over Time
    st.subheader("😊 User Sentiment Over Time")

    # Group by week and sentiment
    sentiment_timeline = filtered_df.groupby(['week', 'Sentiment']).size().reset_index(name='count')

    sentiment_colors = {
        'Positive': '#4CAF50',
        'Neutral': '#9E9E9E',
        'Negative': '#FF4B4B'
    }

    fig5 = px.line(
        sentiment_timeline,
        x='week',
        y='count',
        color='Sentiment',
        color_discrete_map=sentiment_colors,
        markers=True,
        labels={'week': 'Week', 'count': 'Number of Issues'},
        title='Sentiment Trends'
    )
    fig5.update_layout(height=350, hovermode='x unified')
    st.plotly_chart(fig5, use_container_width=True)

    # Sentiment breakdown stats
    col_sent1, col_sent2, col_sent3 = st.columns(3)
    sentiment_counts = filtered_df['Sentiment'].value_counts()

    with col_sent1:
        if 'Negative' in sentiment_counts.index:
            count = sentiment_counts['Negative']
            pct = (count / len(filtered_df)) * 100
            st.metric("😤 Negative", f"{count} ({pct:.1f}%)")

    with col_sent2:
        if 'Neutral' in sentiment_counts.index:
            count = sentiment_counts['Neutral']
            pct = (count / len(filtered_df)) * 100
            st.metric("😐 Neutral", f"{count} ({pct:.1f}%)")

    with col_sent3:
        if 'Positive' in sentiment_counts.index:
            count = sentiment_counts['Positive']
            pct = (count / len(filtered_df)) * 100
            st.metric("😊 Positive", f"{count} ({pct:.1f}%)")

    st.markdown("---")

    # Issue Explorer Section
    st.subheader("🔍 Issue Explorer")

    st.markdown(f"**Showing {len(filtered_df)} issues** (filtered by criteria above)")

    # Display filtered issues
    display_cols = [
        'issue_number', 'title', 'Category', 'Priority',
        'Sentiment', 'Summary', 'L1_Tag', 'L1_Category',
        'L2_Tag', 'L2_Category', 'Confidence', 'Tagging_Notes',
        'Prio Reasoning', 'comments_count', 'created_at', 'html_url'
    ]

    st.dataframe(
        filtered_df[display_cols],
        use_container_width=True,
        height=400,
        column_config={
            "html_url": st.column_config.LinkColumn("GitHub Link"),
            "issue_number": "Issue #",
            "title": "Title",
            "Category": "Category",
            "Priority": "Priority",
            "Sentiment": "Sentiment",
            "Summary": "Summary",
            "L1_Tag": "L1 Tag",
            "L1_Category": "L1 Category",
            "L2_Tag": "L2 Tag",
            "L2_Category": "L2 Category",
            "Confidence": "Confidence",
            "Tagging_Notes": "Tagging Notes",
            "Prio Reasoning": "Priority Reasoning",
            "comments_count": "Comments",
            "created_at": "Created Date"
        }
    )

    # Export filtered data
    if len(filtered_df) > 0:
        st.download_button(
            label="📥 Download Filtered Data (CSV)",
            data=filtered_df.to_csv(index=False).encode('utf-8'),
            file_name=f"filtered_issues_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

    # Most Discussed Issues
    st.markdown("---")
    st.subheader("💬 Most Discussed Issues")
    top_discussed = filtered_df.nlargest(10, 'comments_count')[
        ['issue_number', 'title', 'Category', 'Priority', 'comments_count', 'html_url']
    ]
    st.dataframe(
        top_discussed,
        use_container_width=True,
        column_config={
            "html_url": st.column_config.LinkColumn("GitHub Link"),
            "issue_number": "Issue #",
            "comments_count": "Comments"
        },
        hide_index=True
    )

else:
    st.info("""
    👋 **Welcome to the Claude Code Issues Dashboard!**

    To get started:
    1. Run `extract_github_issues.py` to fetch issues
    2. Process with AI (Claude/Gemini) to add categorization
    3. Save as `Claude_Code_Github_Categorized_ Issue_Tracker.csv`
    4. Run this dashboard: `streamlit run app.py`
    """)
