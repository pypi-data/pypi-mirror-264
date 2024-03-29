import streamlit as st
from __init__ import waterfall_plot

data = [
    {
      "index": 0,
      "label": "test",
      "value": .25,
      "valueString":"25%",
      "accumulated": "0%",
      "accumulatedString":"0%",
      "img":""
    },
    {
      "index": 1,
      "label": "test",
      "value": .15,
      "valueString":"15%",
      "accumulated": "25%",
      "accumulatedString":"25%",
      "img":""
    },
    {
      "index": 2,
      "label": "test",
      "value": .1,
      "valueString":"10%",
      "accumulated": "40%",
      "accumulatedString":"40%",
      "img":""
    },
    {
      "index": 3,
      "label": "test",
      "value": .5,
      "valueString":"0%",
      "accumulated": "0%",
      "accumulatedString":"100%",
      "img":""
    }
  ]

waterfall_plot(data=data)
