import React, {Component, PropTypes} from "react";
import {bindActionCreators} from "redux";
import {connect} from "react-redux";
import PageHeader from "react-bootstrap/lib/PageHeader";
import {performFetchPromise} from "../actions/ApiRequest";
import {showLoading, hideLoading} from "react-redux-loading-bar";
import {LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend} from "recharts"; // Expects that Highcharts was loaded in the code.

function mapStateToProps(state) {
  return {auth: state.auth};
}
function mapDispatchToProps(dispatch) {
  var actions = {showLoading: showLoading, hideLoading: hideLoading};
  return bindActionCreators(actions, dispatch);
}
const data = [
  {
    "dataCZGSMsum": 82328834,
    "dataCZMMSsum": 3137505,
    "_id": "2016-09-01T08:00:00.000Z"
  },
  {
    "dataCZGSMsum": 248974232,
    "dataCZMMSsum": 6972832,
    "_id": "2016-09-01T08:30:00.000Z"
  },
  {
    "dataCZGSMsum": 312828778,
    "dataCZMMSsum": 7325174,
    "_id": "2016-09-01T09:00:00.000Z"
  },
  {
    "dataCZGSMsum": 328882835,
    "dataCZMMSsum": 7942144,
    "_id": "2016-09-01T09:30:00.000Z"
  },
  {
    "dataCZGSMsum": 170633855,
    "dataCZMMSsum": 7936667,
    "_id": "2016-09-01T10:00:00.000Z"
  },
  {
    "dataCZGSMsum": 371073856,
    "dataCZMMSsum": 7826982,
    "_id": "2016-09-01T10:30:00.000Z"
  },
  {
    "dataCZGSMsum": 473387669,
    "dataCZMMSsum": 7621116,
    "_id": "2016-09-01T11:00:00.000Z"
  },
  {
    "dataCZGSMsum": 319436041,
    "dataCZMMSsum": 7378898,
    "_id": "2016-09-01T11:30:00.000Z"
  },
  {
    "dataCZGSMsum": 294367817,
    "dataCZMMSsum": 7073263,
    "_id": "2016-09-01T12:00:00.000Z"
  },
  {
    "dataCZGSMsum": 294250799,
    "dataCZMMSsum": 7032294,
    "_id": "2016-09-01T12:30:00.000Z"
  },
  {
    "dataCZGSMsum": 285894592,
    "dataCZMMSsum": 6803434,
    "_id": "2016-09-01T13:00:00.000Z"
  },
  {
    "dataCZGSMsum": 285057708,
    "dataCZMMSsum": 6673828,
    "_id": "2016-09-01T13:30:00.000Z"
  },
  {
    "dataCZGSMsum": 298390282,
    "dataCZMMSsum": 6316691,
    "_id": "2016-09-01T14:00:00.000Z"
  },
  {
    "dataCZGSMsum": 289264534,
    "dataCZMMSsum": 6479283,
    "_id": "2016-09-01T14:30:00.000Z"
  },
  {
    "dataCZGSMsum": 277107013,
    "dataCZMMSsum": 5972182,
    "_id": "2016-09-01T15:00:00.000Z"
  },
  {
    "dataCZGSMsum": 276862380,
    "dataCZMMSsum": 6340160,
    "_id": "2016-09-01T15:30:00.000Z"
  },
  {
    "dataCZGSMsum": 256209213,
    "dataCZMMSsum": 6028513,
    "_id": "2016-09-01T16:00:00.000Z"
  },
  {
    "dataCZGSMsum": 243389149,
    "dataCZMMSsum": 6144654,
    "_id": "2016-09-01T16:30:00.000Z"
  },
  {
    "dataCZGSMsum": 239984708,
    "dataCZMMSsum": 6141757,
    "_id": "2016-09-01T17:00:00.000Z"
  },
  {
    "dataCZGSMsum": 205745443,
    "dataCZMMSsum": 6130100,
    "_id": "2016-09-01T17:30:00.000Z"
  },
  {
    "dataCZGSMsum": 228138675,
    "dataCZMMSsum": 6417780,
    "_id": "2016-09-01T18:00:00.000Z"
  },
  {
    "dataCZGSMsum": 193801723,
    "dataCZMMSsum": 6215721,
    "_id": "2016-09-01T18:30:00.000Z"
  },
  {
    "dataCZGSMsum": 207541498,
    "dataCZMMSsum": 6726621,
    "_id": "2016-09-01T19:00:00.000Z"
  },
  {
    "dataCZGSMsum": 190268460,
    "dataCZMMSsum": 6255738,
    "_id": "2016-09-01T19:30:00.000Z"
  },
  {
    "dataCZGSMsum": 200446528,
    "dataCZMMSsum": 6362966,
    "_id": "2016-09-01T20:00:00.000Z"
  },
  {
    "dataCZGSMsum": 147316155,
    "dataCZMMSsum": 6033741,
    "_id": "2016-09-01T20:30:00.000Z"
  },
  {
    "dataCZGSMsum": 124593039,
    "dataCZMMSsum": 5187630,
    "_id": "2016-09-01T21:00:00.000Z"
  },
  {
    "dataCZGSMsum": 93075471,
    "dataCZMMSsum": 4300362,
    "_id": "2016-09-01T21:30:00.000Z"
  },
  {
    "dataCZGSMsum": 72268560,
    "dataCZMMSsum": 3540678,
    "_id": "2016-09-01T22:00:00.000Z"
  },
  {
    "dataCZGSMsum": 52498768,
    "dataCZMMSsum": 2376914,
    "_id": "2016-09-01T22:30:00.000Z"
  },
  {
    "dataCZGSMsum": 35151675,
    "dataCZMMSsum": 1799131,
    "_id": "2016-09-01T23:00:00.000Z"
  },
  {
    "dataCZGSMsum": 22443135,
    "dataCZMMSsum": 1124498,
    "_id": "2016-09-01T23:30:00.000Z"
  },
  {
    "dataCZGSMsum": 17951911,
    "dataCZMMSsum": 912526,
    "_id": "2016-09-02T00:00:00.000Z"
  },
  {
    "dataCZGSMsum": 10730246,
    "dataCZMMSsum": 568166,
    "_id": "2016-09-02T00:30:00.000Z"
  },
  {
    "dataCZGSMsum": 8591787,
    "dataCZMMSsum": 448056,
    "_id": "2016-09-02T01:00:00.000Z"
  },
  {
    "dataCZGSMsum": 8123589,
    "dataCZMMSsum": 338832,
    "_id": "2016-09-02T01:30:00.000Z"
  },
  {
    "dataCZGSMsum": 7395715,
    "dataCZMMSsum": 268396,
    "_id": "2016-09-02T02:00:00.000Z"
  },
  {
    "dataCZGSMsum": 5474400,
    "dataCZMMSsum": 231031,
    "_id": "2016-09-02T02:30:00.000Z"
  },
  {
    "dataCZGSMsum": 6085993,
    "dataCZMMSsum": 209630,
    "_id": "2016-09-02T03:00:00.000Z"
  },
  {
    "dataCZGSMsum": 4776180,
    "dataCZMMSsum": 220837,
    "_id": "2016-09-02T03:30:00.000Z"
  },
  {
    "dataCZGSMsum": 5161915,
    "dataCZMMSsum": 223963,
    "_id": "2016-09-02T04:00:00.000Z"
  },
  {
    "dataCZGSMsum": 5769042,
    "dataCZMMSsum": 303360,
    "_id": "2016-09-02T04:30:00.000Z"
  },
  {
    "dataCZGSMsum": 9355311,
    "dataCZMMSsum": 419681,
    "_id": "2016-09-02T05:00:00.000Z"
  },
  {
    "dataCZGSMsum": 15119213,
    "dataCZMMSsum": 602604,
    "_id": "2016-09-02T05:30:00.000Z"
  },
  {
    "dataCZGSMsum": 27790216,
    "dataCZMMSsum": 899642,
    "_id": "2016-09-02T06:00:00.000Z"
  },
  {
    "dataCZGSMsum": 51206244,
    "dataCZMMSsum": 1602647,
    "_id": "2016-09-02T06:30:00.000Z"
  },
  {
    "dataCZGSMsum": 99186847,
    "dataCZMMSsum": 2427107,
    "_id": "2016-09-02T07:00:00.000Z"
  },
  {
    "dataCZGSMsum": 141272000,
    "dataCZMMSsum": 3359216,
    "_id": "2016-09-02T07:30:00.000Z"
  },
  {
    "dataCZGSMsum": 206474201,
    "dataCZMMSsum": 4445687,
    "_id": "2016-09-02T08:00:00.000Z"
  },
  {
    "dataCZGSMsum": 235569681,
    "dataCZMMSsum": 5011441,
    "_id": "2016-09-02T08:30:00.000Z"
  },
  {
    "dataCZGSMsum": 274333931,
    "dataCZMMSsum": 5777705,
    "_id": "2016-09-02T09:00:00.000Z"
  },
  {
    "dataCZGSMsum": 307456978,
    "dataCZMMSsum": 5689666,
    "_id": "2016-09-02T09:30:00.000Z"
  },
  {
    "dataCZGSMsum": 299002737,
    "dataCZMMSsum": 6401249,
    "_id": "2016-09-02T10:00:00.000Z"
  },
  {
    "dataCZGSMsum": 303135592,
    "dataCZMMSsum": 5859604,
    "_id": "2016-09-02T10:30:00.000Z"
  },
  {
    "dataCZGSMsum": 307800150,
    "dataCZMMSsum": 6263972,
    "_id": "2016-09-02T11:00:00.000Z"
  },
  {
    "dataCZGSMsum": 303347059,
    "dataCZMMSsum": 8277183,
    "_id": "2016-09-02T11:30:00.000Z"
  },
  {
    "dataCZGSMsum": 286447572,
    "dataCZMMSsum": 6494629,
    "_id": "2016-09-02T12:00:00.000Z"
  },
  {
    "dataCZGSMsum": 294543023,
    "dataCZMMSsum": 6083657,
    "_id": "2016-09-02T12:30:00.000Z"
  },
  {
    "dataCZGSMsum": 320350308,
    "dataCZMMSsum": 6039117,
    "_id": "2016-09-02T13:00:00.000Z"
  },
  {
    "dataCZGSMsum": 302913787,
    "dataCZMMSsum": 6082888,
    "_id": "2016-09-02T13:30:00.000Z"
  },
  {
    "dataCZGSMsum": 290326547,
    "dataCZMMSsum": 5983165,
    "_id": "2016-09-02T14:00:00.000Z"
  },
  {
    "dataCZGSMsum": 289879662,
    "dataCZMMSsum": 5744779,
    "_id": "2016-09-02T14:30:00.000Z"
  },
  {
    "dataCZGSMsum": 281664942,
    "dataCZMMSsum": 5781538,
    "_id": "2016-09-02T15:00:00.000Z"
  },
  {
    "dataCZGSMsum": 268724855,
    "dataCZMMSsum": 5639706,
    "_id": "2016-09-02T15:30:00.000Z"
  },
  {
    "dataCZGSMsum": 256671027,
    "dataCZMMSsum": 5719385,
    "_id": "2016-09-02T16:00:00.000Z"
  },
  {
    "dataCZGSMsum": 231123251,
    "dataCZMMSsum": 5790439,
    "_id": "2016-09-02T16:30:00.000Z"
  },
  {
    "dataCZGSMsum": 231827612,
    "dataCZMMSsum": 6019972,
    "_id": "2016-09-02T17:00:00.000Z"
  },
  {
    "dataCZGSMsum": 218969333,
    "dataCZMMSsum": 5985179,
    "_id": "2016-09-02T17:30:00.000Z"
  },
  {
    "dataCZGSMsum": 189613417,
    "dataCZMMSsum": 6276784,
    "_id": "2016-09-02T18:00:00.000Z"
  },
  {
    "dataCZGSMsum": 215529721,
    "dataCZMMSsum": 6203465,
    "_id": "2016-09-02T18:30:00.000Z"
  },
  {
    "dataCZGSMsum": 198847919,
    "dataCZMMSsum": 7306877,
    "_id": "2016-09-02T19:00:00.000Z"
  },
  {
    "dataCZGSMsum": 177202284,
    "dataCZMMSsum": 6403341,
    "_id": "2016-09-02T19:30:00.000Z"
  },
  {
    "dataCZGSMsum": 178155420,
    "dataCZMMSsum": 6342308,
    "_id": "2016-09-02T20:00:00.000Z"
  },
  {
    "dataCZGSMsum": 154528883,
    "dataCZMMSsum": 5554913,
    "_id": "2016-09-02T20:30:00.000Z"
  },
  {
    "dataCZGSMsum": 122469872,
    "dataCZMMSsum": 4989822,
    "_id": "2016-09-02T21:00:00.000Z"
  },
  {
    "dataCZGSMsum": 99242521,
    "dataCZMMSsum": 4109510,
    "_id": "2016-09-02T21:30:00.000Z"
  },
  {
    "dataCZGSMsum": 79041671,
    "dataCZMMSsum": 3523551,
    "_id": "2016-09-02T22:00:00.000Z"
  },
  {
    "dataCZGSMsum": 62805584,
    "dataCZMMSsum": 2646829,
    "_id": "2016-09-02T22:30:00.000Z"
  },
  {
    "dataCZGSMsum": 45312767,
    "dataCZMMSsum": 2023656,
    "_id": "2016-09-02T23:00:00.000Z"
  },
  {
    "dataCZGSMsum": 34409379,
    "dataCZMMSsum": 1639968,
    "_id": "2016-09-02T23:30:00.000Z"
  },
  {
    "dataCZGSMsum": 32567418,
    "dataCZMMSsum": 1162749,
    "_id": "2016-09-03T00:00:00.000Z"
  },
  {
    "dataCZGSMsum": 21308011,
    "dataCZMMSsum": 762640,
    "_id": "2016-09-03T00:30:00.000Z"
  },
  {
    "dataCZGSMsum": 17257300,
    "dataCZMMSsum": 686574,
    "_id": "2016-09-03T01:00:00.000Z"
  },
  {
    "dataCZGSMsum": 15463921,
    "dataCZMMSsum": 532503,
    "_id": "2016-09-03T01:30:00.000Z"
  },
  {
    "dataCZGSMsum": 12501271,
    "dataCZMMSsum": 462798,
    "_id": "2016-09-03T02:00:00.000Z"
  },
  {
    "dataCZGSMsum": 10830463,
    "dataCZMMSsum": 398947,
    "_id": "2016-09-03T02:30:00.000Z"
  },
  {
    "dataCZGSMsum": 9802763,
    "dataCZMMSsum": 350561,
    "_id": "2016-09-03T03:00:00.000Z"
  },
  {
    "dataCZGSMsum": 7947553,
    "dataCZMMSsum": 294052,
    "_id": "2016-09-03T03:30:00.000Z"
  },
  {
    "dataCZGSMsum": 7483984,
    "dataCZMMSsum": 307760,
    "_id": "2016-09-03T04:00:00.000Z"
  },
  {
    "dataCZGSMsum": 6436897,
    "dataCZMMSsum": 325119,
    "_id": "2016-09-03T04:30:00.000Z"
  },
  {
    "dataCZGSMsum": 7930209,
    "dataCZMMSsum": 358020,
    "_id": "2016-09-03T05:00:00.000Z"
  },
  {
    "dataCZGSMsum": 8057308,
    "dataCZMMSsum": 460380,
    "_id": "2016-09-03T05:30:00.000Z"
  },
  {
    "dataCZGSMsum": 11660666,
    "dataCZMMSsum": 666549,
    "_id": "2016-09-03T06:00:00.000Z"
  },
  {
    "dataCZGSMsum": 15255200,
    "dataCZMMSsum": 944841,
    "_id": "2016-09-03T06:30:00.000Z"
  },
  {
    "dataCZGSMsum": 26613180,
    "dataCZMMSsum": 1361143,
    "_id": "2016-09-03T07:00:00.000Z"
  },
  {
    "dataCZGSMsum": 43246457,
    "dataCZMMSsum": 1839106,
    "_id": "2016-09-03T07:30:00.000Z"
  },
  {
    "dataCZGSMsum": 67725564,
    "dataCZMMSsum": 2506485,
    "_id": "2016-09-03T08:00:00.000Z"
  },
  {
    "dataCZGSMsum": 95663888,
    "dataCZMMSsum": 3213742,
    "_id": "2016-09-03T08:30:00.000Z"
  },
  {
    "dataCZGSMsum": 125082906,
    "dataCZMMSsum": 3990872,
    "_id": "2016-09-03T09:00:00.000Z"
  },
  {
    "dataCZGSMsum": 145893755,
    "dataCZMMSsum": 4472147,
    "_id": "2016-09-03T09:30:00.000Z"
  },
  {
    "dataCZGSMsum": 160764993,
    "dataCZMMSsum": 5133051,
    "_id": "2016-09-03T10:00:00.000Z"
  },
  {
    "dataCZGSMsum": 156874716,
    "dataCZMMSsum": 6235830,
    "_id": "2016-09-03T10:30:00.000Z"
  },
  {
    "dataCZGSMsum": 156928827,
    "dataCZMMSsum": 5584448,
    "_id": "2016-09-03T11:00:00.000Z"
  },
  {
    "dataCZGSMsum": 160339805,
    "dataCZMMSsum": 5917872,
    "_id": "2016-09-03T11:30:00.000Z"
  },
  {
    "dataCZGSMsum": 141225183,
    "dataCZMMSsum": 5795151,
    "_id": "2016-09-03T12:00:00.000Z"
  },
  {
    "dataCZGSMsum": 138902265,
    "dataCZMMSsum": 5685606,
    "_id": "2016-09-03T12:30:00.000Z"
  },
  {
    "dataCZGSMsum": 146746148,
    "dataCZMMSsum": 6007424,
    "_id": "2016-09-03T13:00:00.000Z"
  },
  {
    "dataCZGSMsum": 136027173,
    "dataCZMMSsum": 6376793,
    "_id": "2016-09-03T13:30:00.000Z"
  },
  {
    "dataCZGSMsum": 130660017,
    "dataCZMMSsum": 6796947,
    "_id": "2016-09-03T14:00:00.000Z"
  },
  {
    "dataCZGSMsum": 125519800,
    "dataCZMMSsum": 6416927,
    "_id": "2016-09-03T14:30:00.000Z"
  },
  {
    "dataCZGSMsum": 129366701,
    "dataCZMMSsum": 6002970,
    "_id": "2016-09-03T15:00:00.000Z"
  },
  {
    "dataCZGSMsum": 124786641,
    "dataCZMMSsum": 6887724,
    "_id": "2016-09-03T15:30:00.000Z"
  },
  {
    "dataCZGSMsum": 130044729,
    "dataCZMMSsum": 7160835,
    "_id": "2016-09-03T16:00:00.000Z"
  },
  {
    "dataCZGSMsum": 125969308,
    "dataCZMMSsum": 7375831,
    "_id": "2016-09-03T16:30:00.000Z"
  },
  {
    "dataCZGSMsum": 131273997,
    "dataCZMMSsum": 7251968,
    "_id": "2016-09-03T17:00:00.000Z"
  },
  {
    "dataCZGSMsum": 141296443,
    "dataCZMMSsum": 7421787,
    "_id": "2016-09-03T17:30:00.000Z"
  },
  {
    "dataCZGSMsum": 138274288,
    "dataCZMMSsum": 7647151,
    "_id": "2016-09-03T18:00:00.000Z"
  },
  {
    "dataCZGSMsum": 131705184,
    "dataCZMMSsum": 7606403,
    "_id": "2016-09-03T18:30:00.000Z"
  },
  {
    "dataCZGSMsum": 146409002,
    "dataCZMMSsum": 7985219,
    "_id": "2016-09-03T19:00:00.000Z"
  },
  {
    "dataCZGSMsum": 160280734,
    "dataCZMMSsum": 7746078,
    "_id": "2016-09-03T19:30:00.000Z"
  },
  {
    "dataCZGSMsum": 142677447,
    "dataCZMMSsum": 7489354,
    "_id": "2016-09-03T20:00:00.000Z"
  },
  {
    "dataCZGSMsum": 125290421,
    "dataCZMMSsum": 6320270,
    "_id": "2016-09-03T20:30:00.000Z"
  },
  {
    "dataCZGSMsum": 104767225,
    "dataCZMMSsum": 5801892,
    "_id": "2016-09-03T21:00:00.000Z"
  },
  {
    "dataCZGSMsum": 79906539,
    "dataCZMMSsum": 5118046,
    "_id": "2016-09-03T21:30:00.000Z"
  },
  {
    "dataCZGSMsum": 70531531,
    "dataCZMMSsum": 4342096,
    "_id": "2016-09-03T22:00:00.000Z"
  },
  {
    "dataCZGSMsum": 58107560,
    "dataCZMMSsum": 3716699,
    "_id": "2016-09-03T22:30:00.000Z"
  },
  {
    "dataCZGSMsum": 43345243,
    "dataCZMMSsum": 3097466,
    "_id": "2016-09-03T23:00:00.000Z"
  },
  {
    "dataCZGSMsum": 36909496,
    "dataCZMMSsum": 2500582,
    "_id": "2016-09-03T23:30:00.000Z"
  },
  {
    "dataCZGSMsum": 31939987,
    "dataCZMMSsum": 2343656,
    "_id": "2016-09-04T00:00:00.000Z"
  },
  {
    "dataCZGSMsum": 21238460,
    "dataCZMMSsum": 1951934,
    "_id": "2016-09-04T00:30:00.000Z"
  },
  {
    "dataCZGSMsum": 19580239,
    "dataCZMMSsum": 1781011,
    "_id": "2016-09-04T01:00:00.000Z"
  },
  {
    "dataCZGSMsum": 14354178,
    "dataCZMMSsum": 1714873,
    "_id": "2016-09-04T01:30:00.000Z"
  },
  {
    "dataCZGSMsum": 14196432,
    "dataCZMMSsum": 1598932,
    "_id": "2016-09-04T02:00:00.000Z"
  },
  {
    "dataCZGSMsum": 12188400,
    "dataCZMMSsum": 1433282,
    "_id": "2016-09-04T02:30:00.000Z"
  },
  {
    "dataCZGSMsum": 10618386,
    "dataCZMMSsum": 1391097,
    "_id": "2016-09-04T03:00:00.000Z"
  },
  {
    "dataCZGSMsum": 7759733,
    "dataCZMMSsum": 1397046,
    "_id": "2016-09-04T03:30:00.000Z"
  },
  {
    "dataCZGSMsum": 6173674,
    "dataCZMMSsum": 1383948,
    "_id": "2016-09-04T04:00:00.000Z"
  },
  {
    "dataCZGSMsum": 6226447,
    "dataCZMMSsum": 1414021,
    "_id": "2016-09-04T04:30:00.000Z"
  },
  {
    "dataCZGSMsum": 6596148,
    "dataCZMMSsum": 1441987,
    "_id": "2016-09-04T05:00:00.000Z"
  },
  {
    "dataCZGSMsum": 6419452,
    "dataCZMMSsum": 1484700,
    "_id": "2016-09-04T05:30:00.000Z"
  },
  {
    "dataCZGSMsum": 6768127,
    "dataCZMMSsum": 1640199,
    "_id": "2016-09-04T06:00:00.000Z"
  },
  {
    "dataCZGSMsum": 10489312,
    "dataCZMMSsum": 1801877,
    "_id": "2016-09-04T06:30:00.000Z"
  },
  {
    "dataCZGSMsum": 16091413,
    "dataCZMMSsum": 2152119,
    "_id": "2016-09-04T07:00:00.000Z"
  },
  {
    "dataCZGSMsum": 24810163,
    "dataCZMMSsum": 2682138,
    "_id": "2016-09-04T07:30:00.000Z"
  },
  {
    "dataCZGSMsum": 40669383,
    "dataCZMMSsum": 3271257,
    "_id": "2016-09-04T08:00:00.000Z"
  },
  {
    "dataCZGSMsum": 63766363,
    "dataCZMMSsum": 3766541,
    "_id": "2016-09-04T08:30:00.000Z"
  },
  {
    "dataCZGSMsum": 93219446,
    "dataCZMMSsum": 4489791,
    "_id": "2016-09-04T09:00:00.000Z"
  },
  {
    "dataCZGSMsum": 114963349,
    "dataCZMMSsum": 5860429,
    "_id": "2016-09-04T09:30:00.000Z"
  },
  {
    "dataCZGSMsum": 130057271,
    "dataCZMMSsum": 5062693,
    "_id": "2016-09-04T10:00:00.000Z"
  },
  {
    "dataCZGSMsum": 136786265,
    "dataCZMMSsum": 5741437,
    "_id": "2016-09-04T10:30:00.000Z"
  },
  {
    "dataCZGSMsum": 138049338,
    "dataCZMMSsum": 6138299,
    "_id": "2016-09-04T11:00:00.000Z"
  },
  {
    "dataCZGSMsum": 129697264,
    "dataCZMMSsum": 6606904,
    "_id": "2016-09-04T11:30:00.000Z"
  },
  {
    "dataCZGSMsum": 130529888,
    "dataCZMMSsum": 6127105,
    "_id": "2016-09-04T12:00:00.000Z"
  },
  {
    "dataCZGSMsum": 123278962,
    "dataCZMMSsum": 6135548,
    "_id": "2016-09-04T12:30:00.000Z"
  },
  {
    "dataCZGSMsum": 128516551,
    "dataCZMMSsum": 6668217,
    "_id": "2016-09-04T13:00:00.000Z"
  },
  {
    "dataCZGSMsum": 122437173,
    "dataCZMMSsum": 6379426,
    "_id": "2016-09-04T13:30:00.000Z"
  },
  {
    "dataCZGSMsum": 120498919,
    "dataCZMMSsum": 6252672,
    "_id": "2016-09-04T14:00:00.000Z"
  },
  {
    "dataCZGSMsum": 121182479,
    "dataCZMMSsum": 6456673,
    "_id": "2016-09-04T14:30:00.000Z"
  },
  {
    "dataCZGSMsum": 122859065,
    "dataCZMMSsum": 6436006,
    "_id": "2016-09-04T15:00:00.000Z"
  },
  {
    "dataCZGSMsum": 124448981,
    "dataCZMMSsum": 6255045,
    "_id": "2016-09-04T15:30:00.000Z"
  },
  {
    "dataCZGSMsum": 140089396,
    "dataCZMMSsum": 6476529,
    "_id": "2016-09-04T16:00:00.000Z"
  },
  {
    "dataCZGSMsum": 137047022,
    "dataCZMMSsum": 6551697,
    "_id": "2016-09-04T16:30:00.000Z"
  },
  {
    "dataCZGSMsum": 130904938,
    "dataCZMMSsum": 6632902,
    "_id": "2016-09-04T17:00:00.000Z"
  },
  {
    "dataCZGSMsum": 149213406,
    "dataCZMMSsum": 6820934,
    "_id": "2016-09-04T17:30:00.000Z"
  },
  {
    "dataCZGSMsum": 152233665,
    "dataCZMMSsum": 7174819,
    "_id": "2016-09-04T18:00:00.000Z"
  },
  {
    "dataCZGSMsum": 162094799,
    "dataCZMMSsum": 6920882,
    "_id": "2016-09-04T18:30:00.000Z"
  },
  {
    "dataCZGSMsum": 167800626,
    "dataCZMMSsum": 8173432,
    "_id": "2016-09-04T19:00:00.000Z"
  },
  {
    "dataCZGSMsum": 168128507,
    "dataCZMMSsum": 7205711,
    "_id": "2016-09-04T19:30:00.000Z"
  },
  {
    "dataCZGSMsum": 146536286,
    "dataCZMMSsum": 6331300,
    "_id": "2016-09-04T20:00:00.000Z"
  },
  {
    "dataCZGSMsum": 127688835,
    "dataCZMMSsum": 6072786,
    "_id": "2016-09-04T20:30:00.000Z"
  },
  {
    "dataCZGSMsum": 99484910,
    "dataCZMMSsum": 5756554,
    "_id": "2016-09-04T21:00:00.000Z"
  },
  {
    "dataCZGSMsum": 79123386,
    "dataCZMMSsum": 6181874,
    "_id": "2016-09-04T21:30:00.000Z"
  },
  {
    "dataCZGSMsum": 53771782,
    "dataCZMMSsum": 5259690,
    "_id": "2016-09-04T22:00:00.000Z"
  },
  {
    "dataCZGSMsum": 49558457,
    "dataCZMMSsum": 4496965,
    "_id": "2016-09-04T22:30:00.000Z"
  },
  {
    "dataCZGSMsum": 30351049,
    "dataCZMMSsum": 3981212,
    "_id": "2016-09-04T23:00:00.000Z"
  },
  {
    "dataCZGSMsum": 20700264,
    "dataCZMMSsum": 2633686,
    "_id": "2016-09-04T23:30:00.000Z"
  },
  {
    "dataCZGSMsum": 14873004,
    "dataCZMMSsum": 2244909,
    "_id": "2016-09-05T00:00:00.000Z"
  },
  {
    "dataCZGSMsum": 9669327,
    "dataCZMMSsum": 1784389,
    "_id": "2016-09-05T00:30:00.000Z"
  },
  {
    "dataCZGSMsum": 7647565,
    "dataCZMMSsum": 1617261,
    "_id": "2016-09-05T01:00:00.000Z"
  },
  {
    "dataCZGSMsum": 7259942,
    "dataCZMMSsum": 1463528,
    "_id": "2016-09-05T01:30:00.000Z"
  },
  {
    "dataCZGSMsum": 6594343,
    "dataCZMMSsum": 1509549,
    "_id": "2016-09-05T02:00:00.000Z"
  },
  {
    "dataCZGSMsum": 6013929,
    "dataCZMMSsum": 1430489,
    "_id": "2016-09-05T02:30:00.000Z"
  },
  {
    "dataCZGSMsum": 5070624,
    "dataCZMMSsum": 1360333,
    "_id": "2016-09-05T03:00:00.000Z"
  },
  {
    "dataCZGSMsum": 4687835,
    "dataCZMMSsum": 1395471,
    "_id": "2016-09-05T03:30:00.000Z"
  },
  {
    "dataCZGSMsum": 4993534,
    "dataCZMMSsum": 1425992,
    "_id": "2016-09-05T04:00:00.000Z"
  },
  {
    "dataCZGSMsum": 5797462,
    "dataCZMMSsum": 1440099,
    "_id": "2016-09-05T04:30:00.000Z"
  },
  {
    "dataCZGSMsum": 11297904,
    "dataCZMMSsum": 1524688,
    "_id": "2016-09-05T05:00:00.000Z"
  },
  {
    "dataCZGSMsum": 15961979,
    "dataCZMMSsum": 1401145,
    "_id": "2016-09-05T05:30:00.000Z"
  },
  {
    "dataCZGSMsum": 27974963,
    "dataCZMMSsum": 1291161,
    "_id": "2016-09-05T06:00:00.000Z"
  },
  {
    "dataCZGSMsum": 54480747,
    "dataCZMMSsum": 1753558,
    "_id": "2016-09-05T06:30:00.000Z"
  },
  {
    "dataCZGSMsum": 98955863,
    "dataCZMMSsum": 2537336,
    "_id": "2016-09-05T07:00:00.000Z"
  },
  {
    "dataCZGSMsum": 154168541,
    "dataCZMMSsum": 4271317,
    "_id": "2016-09-05T07:30:00.000Z"
  },
  {
    "dataCZGSMsum": 214516322,
    "dataCZMMSsum": 5758038,
    "_id": "2016-09-05T08:00:00.000Z"
  },
  {
    "dataCZGSMsum": 247973110,
    "dataCZMMSsum": 7820857,
    "_id": "2016-09-05T08:30:00.000Z"
  },
  {
    "dataCZGSMsum": 282322756,
    "dataCZMMSsum": 6146782,
    "_id": "2016-09-05T09:00:00.000Z"
  },
  {
    "dataCZGSMsum": 289731354,
    "dataCZMMSsum": 6605711,
    "_id": "2016-09-05T09:30:00.000Z"
  },
  {
    "dataCZGSMsum": 311625817,
    "dataCZMMSsum": 7385671,
    "_id": "2016-09-05T10:00:00.000Z"
  },
  {
    "dataCZGSMsum": 293939832,
    "dataCZMMSsum": 7182165,
    "_id": "2016-09-05T10:30:00.000Z"
  },
  {
    "dataCZGSMsum": 324613458,
    "dataCZMMSsum": 7115747,
    "_id": "2016-09-05T11:00:00.000Z"
  },
  {
    "dataCZGSMsum": 286134385,
    "dataCZMMSsum": 7350250,
    "_id": "2016-09-05T11:30:00.000Z"
  },
  {
    "dataCZGSMsum": 282531170,
    "dataCZMMSsum": 7110498,
    "_id": "2016-09-05T12:00:00.000Z"
  },
  {
    "dataCZGSMsum": 290828245,
    "dataCZMMSsum": 7833535,
    "_id": "2016-09-05T12:30:00.000Z"
  },
  {
    "dataCZGSMsum": 299174651,
    "dataCZMMSsum": 7374933,
    "_id": "2016-09-05T13:00:00.000Z"
  },
  {
    "dataCZGSMsum": 298858828,
    "dataCZMMSsum": 8115469,
    "_id": "2016-09-05T13:30:00.000Z"
  },
  {
    "dataCZGSMsum": 316032345,
    "dataCZMMSsum": 8387564,
    "_id": "2016-09-05T14:00:00.000Z"
  },
  {
    "dataCZGSMsum": 307117501,
    "dataCZMMSsum": 8362151,
    "_id": "2016-09-05T14:30:00.000Z"
  },
  {
    "dataCZGSMsum": 307222438,
    "dataCZMMSsum": 8217451,
    "_id": "2016-09-05T15:00:00.000Z"
  },
  {
    "dataCZGSMsum": 294426341,
    "dataCZMMSsum": 8035642,
    "_id": "2016-09-05T15:30:00.000Z"
  },
  {
    "dataCZGSMsum": 286557703,
    "dataCZMMSsum": 7096109,
    "_id": "2016-09-05T16:00:00.000Z"
  },
  {
    "dataCZGSMsum": 265036250,
    "dataCZMMSsum": 6661881,
    "_id": "2016-09-05T16:30:00.000Z"
  },
  {
    "dataCZGSMsum": 252927243,
    "dataCZMMSsum": 7198126,
    "_id": "2016-09-05T17:00:00.000Z"
  },
  {
    "dataCZGSMsum": 227303467,
    "dataCZMMSsum": 8012571,
    "_id": "2016-09-05T17:30:00.000Z"
  },
  {
    "dataCZGSMsum": 198200785,
    "dataCZMMSsum": 8531904,
    "_id": "2016-09-05T18:00:00.000Z"
  },
  {
    "dataCZGSMsum": 215552443,
    "dataCZMMSsum": 7355495,
    "_id": "2016-09-05T18:30:00.000Z"
  },
  {
    "dataCZGSMsum": 198935568,
    "dataCZMMSsum": 6794872,
    "_id": "2016-09-05T19:00:00.000Z"
  },
  {
    "dataCZGSMsum": 177588143,
    "dataCZMMSsum": 6926950,
    "_id": "2016-09-05T19:30:00.000Z"
  },
  {
    "dataCZGSMsum": 174124458,
    "dataCZMMSsum": 8168951,
    "_id": "2016-09-05T20:00:00.000Z"
  },
  {
    "dataCZGSMsum": 142187295,
    "dataCZMMSsum": 7541296,
    "_id": "2016-09-05T20:30:00.000Z"
  },
  {
    "dataCZGSMsum": 107232304,
    "dataCZMMSsum": 5962172,
    "_id": "2016-09-05T21:00:00.000Z"
  },
  {
    "dataCZGSMsum": 82414567,
    "dataCZMMSsum": 5173315,
    "_id": "2016-09-05T21:30:00.000Z"
  },
  {
    "dataCZGSMsum": 66390478,
    "dataCZMMSsum": 4640953,
    "_id": "2016-09-05T22:00:00.000Z"
  },
  {
    "dataCZGSMsum": 46509441,
    "dataCZMMSsum": 3804751,
    "_id": "2016-09-05T22:30:00.000Z"
  },
  {
    "dataCZGSMsum": 28172201,
    "dataCZMMSsum": 3281068,
    "_id": "2016-09-05T23:00:00.000Z"
  },
  {
    "dataCZGSMsum": 19656914,
    "dataCZMMSsum": 2635013,
    "_id": "2016-09-05T23:30:00.000Z"
  },
  {
    "dataCZGSMsum": 15947215,
    "dataCZMMSsum": 1449436,
    "_id": "2016-09-06T00:00:00.000Z"
  },
  {
    "dataCZGSMsum": 8705889,
    "dataCZMMSsum": 496100,
    "_id": "2016-09-06T00:30:00.000Z"
  },
  {
    "dataCZGSMsum": 8091729,
    "dataCZMMSsum": 434727,
    "_id": "2016-09-06T01:00:00.000Z"
  },
  {
    "dataCZGSMsum": 6583360,
    "dataCZMMSsum": 314637,
    "_id": "2016-09-06T01:30:00.000Z"
  },
  {
    "dataCZGSMsum": 7092673,
    "dataCZMMSsum": 287853,
    "_id": "2016-09-06T02:00:00.000Z"
  },
  {
    "dataCZGSMsum": 4834918,
    "dataCZMMSsum": 247044,
    "_id": "2016-09-06T02:30:00.000Z"
  },
  {
    "dataCZGSMsum": 5486077,
    "dataCZMMSsum": 196706,
    "_id": "2016-09-06T03:00:00.000Z"
  },
  {
    "dataCZGSMsum": 4319654,
    "dataCZMMSsum": 255288,
    "_id": "2016-09-06T03:30:00.000Z"
  },
  {
    "dataCZGSMsum": 4884509,
    "dataCZMMSsum": 227397,
    "_id": "2016-09-06T04:00:00.000Z"
  },
  {
    "dataCZGSMsum": 6534768,
    "dataCZMMSsum": 296388,
    "_id": "2016-09-06T04:30:00.000Z"
  },
  {
    "dataCZGSMsum": 8249572,
    "dataCZMMSsum": 335890,
    "_id": "2016-09-06T05:00:00.000Z"
  },
  {
    "dataCZGSMsum": 14800651,
    "dataCZMMSsum": 1360770,
    "_id": "2016-09-06T05:30:00.000Z"
  },
  {
    "dataCZGSMsum": 26960722,
    "dataCZMMSsum": 1867443,
    "_id": "2016-09-06T06:00:00.000Z"
  },
  {
    "dataCZGSMsum": 51245678,
    "dataCZMMSsum": 3884689,
    "_id": "2016-09-06T06:30:00.000Z"
  },
  {
    "dataCZGSMsum": 95815334,
    "dataCZMMSsum": 4987648,
    "_id": "2016-09-06T07:00:00.000Z"
  },
  {
    "dataCZGSMsum": 148912281,
    "dataCZMMSsum": 4952897,
    "_id": "2016-09-06T07:30:00.000Z"
  },
  {
    "dataCZGSMsum": 197183052,
    "dataCZMMSsum": 4558990,
    "_id": "2016-09-06T08:00:00.000Z"
  },
  {
    "dataCZGSMsum": 235048504,
    "dataCZMMSsum": 6069016,
    "_id": "2016-09-06T08:30:00.000Z"
  },
  {
    "dataCZGSMsum": 269582940,
    "dataCZMMSsum": 6795693,
    "_id": "2016-09-06T09:00:00.000Z"
  },
  {
    "dataCZGSMsum": 294277634,
    "dataCZMMSsum": 6916024,
    "_id": "2016-09-06T09:30:00.000Z"
  },
  {
    "dataCZGSMsum": 294567185,
    "dataCZMMSsum": 7249000,
    "_id": "2016-09-06T10:00:00.000Z"
  },
  {
    "dataCZGSMsum": 289923822,
    "dataCZMMSsum": 7568146,
    "_id": "2016-09-06T10:30:00.000Z"
  },
  {
    "dataCZGSMsum": 277360928,
    "dataCZMMSsum": 8014737,
    "_id": "2016-09-06T11:00:00.000Z"
  },
  {
    "dataCZGSMsum": 281624453,
    "dataCZMMSsum": 6876629,
    "_id": "2016-09-06T11:30:00.000Z"
  },
  {
    "dataCZGSMsum": 261239978,
    "dataCZMMSsum": 6554873,
    "_id": "2016-09-06T12:00:00.000Z"
  },
  {
    "dataCZGSMsum": 265104283,
    "dataCZMMSsum": 6693615,
    "_id": "2016-09-06T12:30:00.000Z"
  },
  {
    "dataCZGSMsum": 286015481,
    "dataCZMMSsum": 6199027,
    "_id": "2016-09-06T13:00:00.000Z"
  },
  {
    "dataCZGSMsum": 277238344,
    "dataCZMMSsum": 7132763,
    "_id": "2016-09-06T13:30:00.000Z"
  },
  {
    "dataCZGSMsum": 298545377,
    "dataCZMMSsum": 7165514,
    "_id": "2016-09-06T14:00:00.000Z"
  },
  {
    "dataCZGSMsum": 306559996,
    "dataCZMMSsum": 8353790,
    "_id": "2016-09-06T14:30:00.000Z"
  },
  {
    "dataCZGSMsum": 289959914,
    "dataCZMMSsum": 7876484,
    "_id": "2016-09-06T15:00:00.000Z"
  },
  {
    "dataCZGSMsum": 284988723,
    "dataCZMMSsum": 8431668,
    "_id": "2016-09-06T15:30:00.000Z"
  },
  {
    "dataCZGSMsum": 264600825,
    "dataCZMMSsum": 6558399,
    "_id": "2016-09-06T16:00:00.000Z"
  },
  {
    "dataCZGSMsum": 256282243,
    "dataCZMMSsum": 6971627,
    "_id": "2016-09-06T16:30:00.000Z"
  },
  {
    "dataCZGSMsum": 227189523,
    "dataCZMMSsum": 7572360,
    "_id": "2016-09-06T17:00:00.000Z"
  },
  {
    "dataCZGSMsum": 231707582,
    "dataCZMMSsum": 8433263,
    "_id": "2016-09-06T17:30:00.000Z"
  },
  {
    "dataCZGSMsum": 211126870,
    "dataCZMMSsum": 7791923,
    "_id": "2016-09-06T18:00:00.000Z"
  },
  {
    "dataCZGSMsum": 189461782,
    "dataCZMMSsum": 7773004,
    "_id": "2016-09-06T18:30:00.000Z"
  },
  {
    "dataCZGSMsum": 198797425,
    "dataCZMMSsum": 7414330,
    "_id": "2016-09-06T19:00:00.000Z"
  },
  {
    "dataCZGSMsum": 190546779,
    "dataCZMMSsum": 7898772,
    "_id": "2016-09-06T19:30:00.000Z"
  },
  {
    "dataCZGSMsum": 165365454,
    "dataCZMMSsum": 8028416,
    "_id": "2016-09-06T20:00:00.000Z"
  },
  {
    "dataCZGSMsum": 147837731,
    "dataCZMMSsum": 6953442,
    "_id": "2016-09-06T20:30:00.000Z"
  },
  {
    "dataCZGSMsum": 114550279,
    "dataCZMMSsum": 6578092,
    "_id": "2016-09-06T21:00:00.000Z"
  },
  {
    "dataCZGSMsum": 86503000,
    "dataCZMMSsum": 4747949,
    "_id": "2016-09-06T21:30:00.000Z"
  },
  {
    "dataCZGSMsum": 66490170,
    "dataCZMMSsum": 4729656,
    "_id": "2016-09-06T22:00:00.000Z"
  },
  {
    "dataCZGSMsum": 46883223,
    "dataCZMMSsum": 3802490,
    "_id": "2016-09-06T22:30:00.000Z"
  },
  {
    "dataCZGSMsum": 31179801,
    "dataCZMMSsum": 2279966,
    "_id": "2016-09-06T23:00:00.000Z"
  },
  {
    "dataCZGSMsum": 19697151,
    "dataCZMMSsum": 1179346,
    "_id": "2016-09-06T23:30:00.000Z"
  },
  {
    "dataCZGSMsum": 16490459,
    "dataCZMMSsum": 731133,
    "_id": "2016-09-07T00:00:00.000Z"
  },
  {
    "dataCZGSMsum": 9458722,
    "dataCZMMSsum": 586219,
    "_id": "2016-09-07T00:30:00.000Z"
  },
  {
    "dataCZGSMsum": 7951223,
    "dataCZMMSsum": 435715,
    "_id": "2016-09-07T01:00:00.000Z"
  },
  {
    "dataCZGSMsum": 7764318,
    "dataCZMMSsum": 349318,
    "_id": "2016-09-07T01:30:00.000Z"
  },
  {
    "dataCZGSMsum": 7232114,
    "dataCZMMSsum": 318991,
    "_id": "2016-09-07T02:00:00.000Z"
  },
  {
    "dataCZGSMsum": 5263958,
    "dataCZMMSsum": 260406,
    "_id": "2016-09-07T02:30:00.000Z"
  },
  {
    "dataCZGSMsum": 5169356,
    "dataCZMMSsum": 195627,
    "_id": "2016-09-07T03:00:00.000Z"
  },
  {
    "dataCZGSMsum": 4915465,
    "dataCZMMSsum": 228036,
    "_id": "2016-09-07T03:30:00.000Z"
  },
  {
    "dataCZGSMsum": 4924662,
    "dataCZMMSsum": 221432,
    "_id": "2016-09-07T04:00:00.000Z"
  },
  {
    "dataCZGSMsum": 5338048,
    "dataCZMMSsum": 267492,
    "_id": "2016-09-07T04:30:00.000Z"
  },
  {
    "dataCZGSMsum": 9522605,
    "dataCZMMSsum": 310865,
    "_id": "2016-09-07T05:00:00.000Z"
  },
  {
    "dataCZGSMsum": 14632287,
    "dataCZMMSsum": 505728,
    "_id": "2016-09-07T05:30:00.000Z"
  },
  {
    "dataCZGSMsum": 25135102,
    "dataCZMMSsum": 778191,
    "_id": "2016-09-07T06:00:00.000Z"
  },
  {
    "dataCZGSMsum": 49814852,
    "dataCZMMSsum": 2147405,
    "_id": "2016-09-07T06:30:00.000Z"
  },
  {
    "dataCZGSMsum": 94033990,
    "dataCZMMSsum": 3673837,
    "_id": "2016-09-07T07:00:00.000Z"
  },
  {
    "dataCZGSMsum": 139797813,
    "dataCZMMSsum": 6021097,
    "_id": "2016-09-07T07:30:00.000Z"
  },
  {
    "dataCZGSMsum": 201268464,
    "dataCZMMSsum": 7214284,
    "_id": "2016-09-07T08:00:00.000Z"
  },
  {
    "dataCZGSMsum": 230540749,
    "dataCZMMSsum": 7398205,
    "_id": "2016-09-07T08:30:00.000Z"
  },
  {
    "dataCZGSMsum": 290768426,
    "dataCZMMSsum": 8221591,
    "_id": "2016-09-07T09:00:00.000Z"
  },
  {
    "dataCZGSMsum": 293696755,
    "dataCZMMSsum": 8453831,
    "_id": "2016-09-07T09:30:00.000Z"
  },
  {
    "dataCZGSMsum": 277095484,
    "dataCZMMSsum": 8749643,
    "_id": "2016-09-07T10:00:00.000Z"
  },
  {
    "dataCZGSMsum": 298015930,
    "dataCZMMSsum": 7240220,
    "_id": "2016-09-07T10:30:00.000Z"
  },
  {
    "dataCZGSMsum": 294280006,
    "dataCZMMSsum": 7101626,
    "_id": "2016-09-07T11:00:00.000Z"
  },
  {
    "dataCZGSMsum": 272853159,
    "dataCZMMSsum": 7354977,
    "_id": "2016-09-07T11:30:00.000Z"
  },
  {
    "dataCZGSMsum": 277982324,
    "dataCZMMSsum": 7373575,
    "_id": "2016-09-07T12:00:00.000Z"
  },
  {
    "dataCZGSMsum": 256219585,
    "dataCZMMSsum": 7025651,
    "_id": "2016-09-07T12:30:00.000Z"
  },
  {
    "dataCZGSMsum": 290226547,
    "dataCZMMSsum": 7626405,
    "_id": "2016-09-07T13:00:00.000Z"
  },
  {
    "dataCZGSMsum": 294161683,
    "dataCZMMSsum": 7934129,
    "_id": "2016-09-07T13:30:00.000Z"
  },
  {
    "dataCZGSMsum": 306998102,
    "dataCZMMSsum": 7505233,
    "_id": "2016-09-07T14:00:00.000Z"
  },
  {
    "dataCZGSMsum": 297758322,
    "dataCZMMSsum": 7495259,
    "_id": "2016-09-07T14:30:00.000Z"
  },
  {
    "dataCZGSMsum": 293891333,
    "dataCZMMSsum": 7168805,
    "_id": "2016-09-07T15:00:00.000Z"
  },
  {
    "dataCZGSMsum": 293400403,
    "dataCZMMSsum": 8355758,
    "_id": "2016-09-07T15:30:00.000Z"
  },
  {
    "dataCZGSMsum": 268545809,
    "dataCZMMSsum": 8208263,
    "_id": "2016-09-07T16:00:00.000Z"
  },
  {
    "dataCZGSMsum": 255739883,
    "dataCZMMSsum": 7857576,
    "_id": "2016-09-07T16:30:00.000Z"
  },
  {
    "dataCZGSMsum": 252433788,
    "dataCZMMSsum": 7802926,
    "_id": "2016-09-07T17:00:00.000Z"
  },
  {
    "dataCZGSMsum": 205477510,
    "dataCZMMSsum": 6694838,
    "_id": "2016-09-07T17:30:00.000Z"
  },
  {
    "dataCZGSMsum": 219428011,
    "dataCZMMSsum": 6486651,
    "_id": "2016-09-07T18:00:00.000Z"
  },
  {
    "dataCZGSMsum": 219368349,
    "dataCZMMSsum": 5956033,
    "_id": "2016-09-07T18:30:00.000Z"
  },
  {
    "dataCZGSMsum": 190183066,
    "dataCZMMSsum": 8279083,
    "_id": "2016-09-07T19:00:00.000Z"
  },
  {
    "dataCZGSMsum": 199192203,
    "dataCZMMSsum": 7166560,
    "_id": "2016-09-07T19:30:00.000Z"
  },
  {
    "dataCZGSMsum": 182900861,
    "dataCZMMSsum": 7121731,
    "_id": "2016-09-07T20:00:00.000Z"
  },
  {
    "dataCZGSMsum": 155134874,
    "dataCZMMSsum": 6186135,
    "_id": "2016-09-07T20:30:00.000Z"
  },
  {
    "dataCZGSMsum": 120343243,
    "dataCZMMSsum": 5206089,
    "_id": "2016-09-07T21:00:00.000Z"
  },
  {
    "dataCZGSMsum": 90309066,
    "dataCZMMSsum": 4103931,
    "_id": "2016-09-07T21:30:00.000Z"
  },
  {
    "dataCZGSMsum": 66931121,
    "dataCZMMSsum": 3287457,
    "_id": "2016-09-07T22:00:00.000Z"
  },
  {
    "dataCZGSMsum": 52110680,
    "dataCZMMSsum": 2443947,
    "_id": "2016-09-07T22:30:00.000Z"
  },
  {
    "dataCZGSMsum": 34015576,
    "dataCZMMSsum": 2020442,
    "_id": "2016-09-07T23:00:00.000Z"
  },
  {
    "dataCZGSMsum": 22872880,
    "dataCZMMSsum": 1128113,
    "_id": "2016-09-07T23:30:00.000Z"
  },
  {
    "dataCZGSMsum": 16819338,
    "dataCZMMSsum": 744077,
    "_id": "2016-09-08T00:00:00.000Z"
  },
  {
    "dataCZGSMsum": 11034207,
    "dataCZMMSsum": 523888,
    "_id": "2016-09-08T00:30:00.000Z"
  },
  {
    "dataCZGSMsum": 8720570,
    "dataCZMMSsum": 434352,
    "_id": "2016-09-08T01:00:00.000Z"
  },
  {
    "dataCZGSMsum": 7474400,
    "dataCZMMSsum": 325594,
    "_id": "2016-09-08T01:30:00.000Z"
  },
  {
    "dataCZGSMsum": 6910796,
    "dataCZMMSsum": 268820,
    "_id": "2016-09-08T02:00:00.000Z"
  },
  {
    "dataCZGSMsum": 6715300,
    "dataCZMMSsum": 241897,
    "_id": "2016-09-08T02:30:00.000Z"
  },
  {
    "dataCZGSMsum": 5150432,
    "dataCZMMSsum": 208126,
    "_id": "2016-09-08T03:00:00.000Z"
  },
  {
    "dataCZGSMsum": 5071330,
    "dataCZMMSsum": 206347,
    "_id": "2016-09-08T03:30:00.000Z"
  },
  {
    "dataCZGSMsum": 4813728,
    "dataCZMMSsum": 222659,
    "_id": "2016-09-08T04:00:00.000Z"
  },
  {
    "dataCZGSMsum": 5938663,
    "dataCZMMSsum": 257909,
    "_id": "2016-09-08T04:30:00.000Z"
  },
  {
    "dataCZGSMsum": 9179842,
    "dataCZMMSsum": 414197,
    "_id": "2016-09-08T05:00:00.000Z"
  },
  {
    "dataCZGSMsum": 13422356,
    "dataCZMMSsum": 573076,
    "_id": "2016-09-08T05:30:00.000Z"
  },
  {
    "dataCZGSMsum": 26308083,
    "dataCZMMSsum": 865667,
    "_id": "2016-09-08T06:00:00.000Z"
  },
  {
    "dataCZGSMsum": 50631753,
    "dataCZMMSsum": 1497974,
    "_id": "2016-09-08T06:30:00.000Z"
  },
  {
    "dataCZGSMsum": 95240881,
    "dataCZMMSsum": 2251843,
    "_id": "2016-09-08T07:00:00.000Z"
  },
  {
    "dataCZGSMsum": 145106954,
    "dataCZMMSsum": 3656024,
    "_id": "2016-09-08T07:30:00.000Z"
  },
  {
    "dataCZGSMsum": 197606087,
    "dataCZMMSsum": 7317630,
    "_id": "2016-09-08T08:00:00.000Z"
  },
  {
    "dataCZGSMsum": 234815905,
    "dataCZMMSsum": 8046679,
    "_id": "2016-09-08T08:30:00.000Z"
  },
  {
    "dataCZGSMsum": 286685084,
    "dataCZMMSsum": 8418726,
    "_id": "2016-09-08T09:00:00.000Z"
  },
  {
    "dataCZGSMsum": 281231438,
    "dataCZMMSsum": 7976798,
    "_id": "2016-09-08T09:30:00.000Z"
  },
  {
    "dataCZGSMsum": 294364902,
    "dataCZMMSsum": 8583570,
    "_id": "2016-09-08T10:00:00.000Z"
  },
  {
    "dataCZGSMsum": 293755362,
    "dataCZMMSsum": 8832310,
    "_id": "2016-09-08T10:30:00.000Z"
  },
  {
    "dataCZGSMsum": 286025554,
    "dataCZMMSsum": 8020480,
    "_id": "2016-09-08T11:00:00.000Z"
  },
  {
    "dataCZGSMsum": 277213494,
    "dataCZMMSsum": 7254968,
    "_id": "2016-09-08T11:30:00.000Z"
  },
  {
    "dataCZGSMsum": 256680531,
    "dataCZMMSsum": 7556557,
    "_id": "2016-09-08T12:00:00.000Z"
  },
  {
    "dataCZGSMsum": 269289501,
    "dataCZMMSsum": 8497763,
    "_id": "2016-09-08T12:30:00.000Z"
  },
  {
    "dataCZGSMsum": 286198075,
    "dataCZMMSsum": 8383894,
    "_id": "2016-09-08T13:00:00.000Z"
  },
  {
    "dataCZGSMsum": 290145538,
    "dataCZMMSsum": 8446950,
    "_id": "2016-09-08T13:30:00.000Z"
  },
  {
    "dataCZGSMsum": 294287648,
    "dataCZMMSsum": 8257501,
    "_id": "2016-09-08T14:00:00.000Z"
  },
  {
    "dataCZGSMsum": 289761452,
    "dataCZMMSsum": 8210016,
    "_id": "2016-09-08T14:30:00.000Z"
  },
  {
    "dataCZGSMsum": 298516121,
    "dataCZMMSsum": 8158987,
    "_id": "2016-09-08T15:00:00.000Z"
  },
  {
    "dataCZGSMsum": 281219535,
    "dataCZMMSsum": 7121605,
    "_id": "2016-09-08T15:30:00.000Z"
  },
  {
    "dataCZGSMsum": 256035036,
    "dataCZMMSsum": 6579973,
    "_id": "2016-09-08T16:00:00.000Z"
  },
  {
    "dataCZGSMsum": 260648305,
    "dataCZMMSsum": 6189616,
    "_id": "2016-09-08T16:30:00.000Z"
  },
  {
    "dataCZGSMsum": 244368544,
    "dataCZMMSsum": 6327743,
    "_id": "2016-09-08T17:00:00.000Z"
  },
  {
    "dataCZGSMsum": 218672546,
    "dataCZMMSsum": 6342631,
    "_id": "2016-09-08T17:30:00.000Z"
  },
  {
    "dataCZGSMsum": 210736712,
    "dataCZMMSsum": 7766505,
    "_id": "2016-09-08T18:00:00.000Z"
  },
  {
    "dataCZGSMsum": 215249208,
    "dataCZMMSsum": 7878069,
    "_id": "2016-09-08T18:30:00.000Z"
  },
  {
    "dataCZGSMsum": 198922297,
    "dataCZMMSsum": 9616378,
    "_id": "2016-09-08T19:00:00.000Z"
  },
  {
    "dataCZGSMsum": 199248631,
    "dataCZMMSsum": 7842764,
    "_id": "2016-09-08T19:30:00.000Z"
  },
  {
    "dataCZGSMsum": 187518677,
    "dataCZMMSsum": 7250775,
    "_id": "2016-09-08T20:00:00.000Z"
  },
  {
    "dataCZGSMsum": 164898361,
    "dataCZMMSsum": 6517280,
    "_id": "2016-09-08T20:30:00.000Z"
  },
  {
    "dataCZGSMsum": 123344337,
    "dataCZMMSsum": 5525891,
    "_id": "2016-09-08T21:00:00.000Z"
  },
  {
    "dataCZGSMsum": 92997718,
    "dataCZMMSsum": 4293253,
    "_id": "2016-09-08T21:30:00.000Z"
  },
  {
    "dataCZGSMsum": 68346655,
    "dataCZMMSsum": 3212392,
    "_id": "2016-09-08T22:00:00.000Z"
  },
  {
    "dataCZGSMsum": 52897685,
    "dataCZMMSsum": 2365961,
    "_id": "2016-09-08T22:30:00.000Z"
  },
  {
    "dataCZGSMsum": 24201103,
    "dataCZMMSsum": 884303,
    "_id": "2016-09-08T23:00:00.000Z"
  }
]
const config = {
  /* HighchartsConfig */
};

class DataFlow extends Component {

  constructor() {
    super();
    this.state = {};
  }

  componentWillMount() {
    this.loadData();
  }

  loadData() {
    var myInit = {
      method: 'POST',
      body: {
        "from": "2016-09-01T08:15:00.000Z",
        "to": "2016-09-08T23:17:00.000Z",
        "aggregation": {
          "sum": ["data.CZ.GSM.sum", "data.CZ.MMS.sum"]
        }
      }
    };
    var that = this;
    this.props.showLoading();
    performFetchPromise("/data/dev", myInit).then(this.createRelativeValues).then(result=> {
      that.setState({response: result});
      that.props.hideLoading();
    });
  }


  render() {

    return <div>
      <div className="col-lg-12">
        <PageHeader>DataFlow</PageHeader>
      </div>

      <div className="col-lg-12">
        <h2>asdasd</h2>
        { this.state.response &&
        <LineChart width={600} height={300} data={this.state.response.data}>
          <XAxis dataKey="_id"/>
          <YAxis/>
          <Tooltip/>
          <Legend />
          <Line type="basis" dataKey="dataCZGSMsum" stroke="red" dot={false} activeDot={true}
                isAnimationActive={false}/>
          <Line type="basis" dataKey="dataCZMMSsum" stroke="blue" dot={false} activeDot={true}
                isAnimationActive={false}/>
        </LineChart>
        }
      </div>

      <div className="row ng-scope">

      </div>


    </div>
  }


  static createRelativeValues(result) {
    var metadata = result.metadata
    for (let v in metadata) {
      metadata[v].diff = metadata[v].max - metadata[v].min
    }
    for (let row of result.data) {
      console.log(row)
      for (let k in metadata) {
        var o = metadata[k]
        row[k + "_relative"] = (row[k] - o.min) / o.diff
      }
    }
    return result;
  }
}
DataFlow = connect(mapStateToProps, mapDispatchToProps)(DataFlow)
export default DataFlow