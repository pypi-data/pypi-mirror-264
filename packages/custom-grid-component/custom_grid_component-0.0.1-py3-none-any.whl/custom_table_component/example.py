import streamlit as st
from __init__ import my_component


st.set_page_config(layout="wide")


tableData = [
    {
      "index": 0,
      "column": "Role",
      "rowData": [
        {
          "index": "All",
        },
        {
          "index": "Marksman",
        },
      ]
    },
    {
      "index": 1,
      "column": "Final damage",
      "rowData": [
        {
          "index": "All",
          "data": [
            { "index": 0, "dmgVal": 300, "dmgValPer": "40%", "color": "red" },
            { "index": 1, "dmgVal": 300, "dmgValPer": "20%", "color": "blue" },
            { "index": 2, "dmgVal": 300, "dmgValPer": "20%", "color": "pink" },
          ]
        },
        {
          "index": "Marksman",
          "data": [
            { "index": 0, "dmgVal": 300, "dmgValPer": "40%", "color": "red" },
            { "index": 1, "dmgVal": 300, "dmgValPer": "20%", "color": "blue" },
            { "index": 2, "dmgVal": 300, "dmgValPer": "20%", "color": "pink" },
          ]
        },
      ]
    },
    {
      "index": 2,
      "column": "Non Elemental damage",
      "rowData": [
        {
          "index": "All",
          "data": [
            { "index": 0, "dmgVal": 300, "dmgValPer": "40%" },
            { "index": 1, "dmgVal": 300, "dmgValPer": "20%" },
            { "index": 2, "dmgVal": 300, "dmgValPer": "20%" },
          ]
        },
        {
          "index": "Marksman",
          "data": [
            { "index": 0, "dmgVal": 300, "dmgValPer": "40%" },
            { "index": 1, "dmgVal": 300, "dmgValPer": "20%" },
            { "index": 2, "dmgVal": 300, "dmgValPer": "20%" },
          ]
        },
      ]
    },
    {
      "index": 3,
      "column": "Active Passive damage",
      "rowData": [
        {
          "index": "All",
          "data": [
            { "index": 0, "dmgVal": 300, "dmgValPer": "40%" },
            { "index": 1, "dmgVal": 300, "dmgValPer": "20%" },
            { "index": 2, "dmgVal": 300, "dmgValPer": "20%" },
          ]
        },
        {
          "index": "Marksman",
          "data": [
            { "index": 0, "dmgVal": 300, "dmgValPer": "40%" },
            { "index": 1, "dmgVal": 300, "dmgValPer": "20%" },
            { "index": 2, "dmgVal": 300, "dmgValPer": "20%" },
          ]
        },
      ]
    },
    {
      "index": 4,
      "column": "Frequency hits",
      "rowData": [
        {
          "index": "All",
          "data": [
            { "index": 0, "dmgVal": 300, "dmgValPer": "40%" },
            { "index": 1, "dmgVal": 300, "dmgValPer": "20%" },
            { "index": 2, "dmgVal": 300, "dmgValPer": "20%" },
          ]
        },
        {
          "index": "Marksman",
          "data": [
            { "index": 0, "dmgVal": 300, "dmgValPer": "40%" },
            { "index": 1, "dmgVal": 300, "dmgValPer": "20%" },
            { "index": 2, "dmgVal": 300, "dmgValPer": "20%" },
          ]
        },
      ]
    },
  ]


Legends=[
  {
      "index": "Non Elemental Damage",
      "data": [
        { "index": 0, "dmgValPer": "0", "label": "", "color": "" },
        { "index": 1, "dmgValPer": "0", "label": "", "color": "" },
        { "index": 2, "dmgValPer": "0", "label": "", "color": "" },
      ]
    },
    {
      "index": "Final Damage",
      "data": [
        { "index": 0, "dmgValPer": "30", "label": "Base", "color": "red" },
        { "index": 1, "dmgValPer": "30", "label": "Extra", "color": "blue" },
        { "index": 2, "dmgValPer": "30", "label": "Sustained", "color": "pink" },
      ]
    },
    {
      "index": "Non Elemental Damage",
      "data": [
        { "index": 0, "dmgValPer": "30", "label": "Base", "color": "red" },
        { "index": 1, "dmgValPer": "30", "label": "Extra", "color": "blue" },
        { "index": 2, "dmgValPer": "30", "label": "Sustained", "color": "pink" },
      ]
    },
    {
      "index": "Non Elemental Damage",
      "data": [
        { "index": 0, "dmgValPer": "30", "label": "Base", "color": "red" },
        { "index": 1, "dmgValPer": "30", "label": "Extra", "color": "blue" },
        { "index": 2, "dmgValPer": "30", "label": "Sustained", "color": "pink" },
      ]
    },
    {
      "index": "Non Elemental Damage",
      "data": [
        { "index": 0, "dmgValPer": "30", "label": "Base", "color": "red" },
        { "index": 1, "dmgValPer": "30", "label": "Extra", "color": "blue" },
        { "index": 2, "dmgValPer": "30", "label": "Sustained", "color": "pink" },
      ]
    },
  ]

with st.columns([1,3,1])[1]:
    my_component(tableData=tableData, Legends=Legends, chartType="bar")



