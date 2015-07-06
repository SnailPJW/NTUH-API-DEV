# NTUH API


## I. Error Codes and Error Messages
---
###1. General cases

- **HTTP401** 101: 帳號密碼錯誤

- **HTTP401** 102: SessionKey 過期

- **HTTP403** 103: 無存取權限

- **HTTP404** 104: 請求之資料不存在 (如不存在指定之排程或醫令藥囑)


###2. Patient api relateds

- **HTTP404** 301: 不存在指定之病患

- **HTTP403** 302: 不可瀏覽指定之病患

###3. Bulletin api related

- **HTTP400** 701: 缺少參數 xxx

- **HTTP400** 702: 參數 xxx 型態錯誤。

###4. Order/Medication/Scheduling/Blood related api

- **HTTP400** 801: [排程] 指定之排程順序無法選取

- **HTTP400** 802: [醫囑] 醫囑相關內容需要修改 細節提示用 message 回傳，不通過的 order request 會回傳對應的 tag 至 failed list 中

- **HTTP400** 803: [藥囑] 藥囑事前檢核流程使用

- **HTTP400** 804: [藥囑] 藥囑事後檢核流程使用


## II. Order Related APIs
---
### 1. OrderCode, OrderRecordId

- Since the original TREORDERCODE and ORDERIDSE is not unique
- OrderCode = **{OrderType}{TREORDERCODE}** (etc. T12345678)
- OrderRecordId = **{OrderType}{ORDERIDSE}** (etc. T00010012001)


### 2. 更新醫療記錄之問題清單答案

- API: */account/{accountNo}/orderRecord/{orderRecordId}/questionary{?limit,offset,sessionKey}*

- method: **PUT**

- parameters: key/value_type should be the **returnKey**/[return_value]:

	** return_value:**
	- for type S, M: the array contains option.returnValue(s)
	- for type D: timestamp (number)
	- for type T, P: string

### 3. 開立醫囑或修改醫囑的 Error Response

		+ Response XXX (application/json)
		{
			"error": 802,
			"message": "PUT_THE_ERROR_MESSAGE_HERE",
			"failed": [
				"1",			// [string] the tag of the specific failed order
				"2",			// [string] the tag of the specific failed order
				...
			]
		}

## III. Medication Related APIs
---
###1. The string format for SpecialDoseOptions [/medication/specialDoseOptions]
- For example:

		"take __{%f:dose1}__mg in the morning, take __{%f:dose2}__mg in the afternoon"

  will generate following element on the user interface:

  ** take `(  )`mg in the morning, take `(  )`mg in the afternoon **

- If the user fill the input box like this:

  ** take `( 0.1 )`mg in the morning, take `( 0.5 )`mg in the afternoon **

  will return with the following content:

		{
			"dose1": 0.1,
	    	"dose2": 0.5
		}

- Description: the pattern contains two parts: **[data_type]** : **[data_key]**, and should be encapsulated by `__{` and `}__`

- **data_key** Rules:

  should contains only [0-9a-zA-Z] **WITHOUT** any special characters

- **data_type** Options:

|           Type          | Syntax |                         Description                        |
|:-----------------------:|:------:|:----------------------------------------------------------:|
| number                  |   %f   | The input box specifically for the integer or the float.   |
| text                    |   %s   | The input box for plain text content.                      |
| single selection item   |   %p   | Define the option for single selection.                    |
| multiple selection item |   %m   | Define the option for multiple selection.                  |
| hour picker             |   %h   | The dropdown menu for selecting specific hour in a day.    |


## IV. API Development Tools
---
### 1. Usage:
- Update the api version (sync with the git tag):
		python main.py version_update	// updated the version if necessary

- Generate the apipary.apib from latest apib files:

		python main.py compile

- Parameters for each command can be found by using **-h**

### 2. Procedure:
- Modify the corresponding apiary file(s)
- Change the git tag & run version_update if necessary
- Compile to generate the latest apiary.apib
- git push to push the latest apipary.apib to the main branch
