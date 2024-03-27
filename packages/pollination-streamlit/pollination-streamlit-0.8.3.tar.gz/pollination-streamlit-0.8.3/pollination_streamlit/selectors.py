import streamlit as st

from pollination_io.api.client import ApiClient
from .authentication import get_api_client as _get_api_client
from pollination_io.interactors import Job, Run

def get_api_client(st_element: st = st) -> ApiClient:

    client = _get_api_client()

    # fix extra_streamlit_components bug
    st.markdown(
    """ 
    <style>
        .element-container:has(iframe[height="0"]) { display: block; }
        .element-container:has(iframe[title="extra_streamlit_components.CookieManager.cookie_manager"]) { display: none; }
    </style>
    """,
        unsafe_allow_html=True,
    )

    if not client.is_authenticated:
        st.warning(
            'The app failed to find your Pollination account information. '
            'Try to refresh the page! If that did not solve the problem, try using '
            'a Pollination API key.'
        )
        client.api_token = st_element.text_input(
            'Enter Pollination APIKEY', type='password',
            help=':bulb: You only need an API Key to access private projects. '
            'If you do not have a key already go to the settings tab under your '
            'profile to generate one.'
        )

    return client


def job_selector(
    client: ApiClient, label: str = 'Job URL',
    default: str = None, help: str = None
) -> Job:
    job_url = st.text_input(label=label, value=default, help=help)
    if not job_url or job_url == 'None':
        return None

    url_split = job_url.split('/')
    job_id = url_split[-1]
    project = url_split[-3]
    owner = url_split[-5]

    return Job(owner, project, job_id, client)


def run_selector(
    client: ApiClient, label: str = 'Run URL',
    default: str = None, help: str = None
) -> Run:
    run_url = st.text_input(label=label, value=default, help=help)
    if not run_url or run_url == 'None':
        return None

    url_split = run_url.split('/')
    run_id = url_split[-1]
    job_id = url_split[-3]
    project = url_split[-5]
    owner = url_split[-7]

    return Run(owner, project, job_id, run_id, client)
