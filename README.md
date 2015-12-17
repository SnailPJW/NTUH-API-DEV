# NTUH API


## I. Error Codes and Error Messages
---
###1. General cases

- **HTTP401** 101: 帳號密碼錯誤

- **HTTP401** 102: SessionKey 過期

- **HTTP403** 103: 無存取權限

- **HTTP404** 104: 請求之資料不存在 (如不存在指定之排程或醫令藥囑)


###2. Patient api related

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

- **HTTP400** 805: [藥囑] 搜尋藥品為不可在平板開立之藥品

- **HTTP400** 806: [藥囑] 藥品開立/修改內容有誤 需要回到原本畫面更正

- **HTTP400** 807: [確認] 指定之某個壹囑



## II. Order Related APIs
---
### 1. OrderCode, OrderRecordId

- Since the original TREORDERCODE and ORDERIDSE is not unique
- OrderCode = **{hospitalCode}_{TREORDERCODE}_{orderType}** (etc. T0_12345678_T)
- OrderRecordId = **{OrderType}{ORDERIDSE}** (etc. T00010012001)

### 2. MedicationCode
- Since the original TREORDERCODE and ORDERIDSE is not unique
- MedicationCode = **{hospitalCode}_{TREORDERCODE}_{medicationType}** (etc. T0_12345678_T)
- MedicationRecordId = **{OrderType}{ORDERIDSE}** (etc. T00010012001)

### 3. 醫令介面常用清單 (static dictionaries)
- API: */order/statics/dictionary/{dictionaryId}*
- 用來取得 1) 大型常用字彙 2) 介面上下拉式選單的內容 3) 頻率表或是階段等 id 與 title 之對照表
- Example: 影像醫學介面上所需的選項

		{
			"content": [
				{
					"title": "with contrast",               // [string] 要顯示在介面上的內容
					"code": "mri_dic001_001",          		// [string, optional] 如果是需回傳的項目時回傳的值
					"note": "無法開立此MRI"          		 // [string, optional] 如果選取時需要顯示的額外提示 (如影像醫學的介面)
				},
				{
					"title": "without contrast",            // [string] 要顯示在介面上的內容
					"returnKey": "mri_dic001_002"           // [string, optional] 如果是需回傳的項目時回傳的值
				},
				...
			]
		}

- Example: 問答題常用字彙

		{
			"content": [
				{
					"title": "台大醫院本院"
				},
				{
					"title": "台大醫院竹東分院"
				},
				{
					"title": "台大醫院雲林分院"
				},
				...
			]
		}

- Example: 階段對照表

		{
			"content": [
				{
					"title": "STAT",
					"code": "order_stage_stat"
				},
				{
					"title": "一般",
					"code": "order_sage_normal"
				},
				...
			]
		}

- Example: 科部清單

		{
			"content": [
				{
					"title": "內科",
					"code": "DEPT_001"
				},
				{
					"title": "外科",
					"code": "DEPT_002"
				}
			]
		}


### 4. 更新醫療記錄之問題清單答案

- API: */account/{accountNo}/orderRecord/{orderRecordId}/questionary{?limit,offset,sessionKey}*

- method: **PUT**

- parameters: key/value_type should be the **returnKey**/[return_value]:

	** return_value:**
	- for type S, M: the array contains option.returnValue(s)
	- for type D: timestamp (number)
	- for type T, P: string

### 5. 開立醫囑或修改醫囑的 Error Response

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

		"take __{%f:dose1}__ __{%u}__ in the morning, take __{%f:dose2}__ __{%u}__ in the afternoon"

  will generate following element on the user interface (while the dose unit is mg):

  ** take `(  )` mg in the morning, take `(  )` mg in the afternoon **

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
| time picker             |   %t   | The dropdown menu for selecting specific hour in a day.    |
| unit             		  |   %u   | Indicate the place where to put the "dose unit"            |

## IV. Parameters (chartNo, accountNo, hospitalCode, and IOEtag)
---
### 1. chartNo & accountNo
- The new accountNo (related to the specified chartNo) will be created when the corresponding patient had been 1) transferred to different branches, 2)  every time he/she send to the hospital, or 3) transferred from ER to weds.
- Cannot get the date time related info when the latest accountNo had been "attached" to the corresponding chartNo.
- Getting the accountNo (*when creating new orders*):
using the edge: [/patients/{chartNo}/accounts{?sessionKey}]()
- Getting the accountNo (*when modifing the orders*):
fetching the accountNo which had been used when creating the order(s) from respone of the edge:
[/patients/{chartNo}/order{?sessionKey,modifiable=true}]()

### 2. IOEtag, hospitalCode, and the accountNo
- **IOETag**: should be the first chart of the accountNo
- **hospitalCode**: the combination of the 4th and the 5th characters
- in short: accountNo = [IOETag]xx[hospitalCode]xxxxx
- for instance: *E15T07315840*: *IOETag = E* and *hospitalCode = T0*

### 3. OrderCode, hospitalCode, typeCode
- OrderCode = [hospitalCode]_[RealOrderCode]_[typeCode]

## V: Report Links
---
### 取得url頁面 (html)
GET reportLink/RemoveSession?sessionKey={sessionKey}&url={url}

### 病程記錄
GET reportLink/progressNote/{noteType}/{accountIDSE}/{version}/{seqNo}?sessionKey={sessionKey}

### 急診病程
GET reportLink/emgProgressNote/{noteType}/{accountIDSE}/{version}/{seqNo}?sessionKey={sessionKey}

### 入院記錄
GET reportLink/admissionNote/{accountIDSE}/{version}/{seqNo}/{completeFlag}?sessionKey={sessionKey}

### 照會
GET reportLink/notifyRecord/{notifyIDSE}?sessionKey={sessionKey}

### 手術記錄
GET reportLink/opNote/{OPIDSE}?sessionKey={sessionKey}

### 藥師記錄
GET reportLink/pharmacyNote/{accountidse}?sessionKey={sessionKey}

### 抓簽章的PDF
GET reportLink/signaturePDF/{emrIndexIDSE}/{emrDocCode}?sessionKey={sessionKey}

### 急診檢傷記錄
GET reportLink/triageNote/{accountidse}/{accountSeqNo}?sessionKey={sessionKey}

### 急診來診記錄
GET reportLink/emgAdmissionNote/{accountidse}/{accountSeqNo}?sessionKey={sessionKey}

### 藥敏試驗
GET reportLink/antiBiotics/{deptCode}/{logDateTime}/{loginNo}/{specimenNo}?sessionKey={sessionKey}

### 取得url頁面 (html)
GET reportLink?sessionKey={sessionKey}&url={url}



## VI. UI elements:
---
### 1. Types:
...

### 2. Examples
...

## VI. API Development Tools
---
### 1. Usage:
- Update the api version (sync with the git tag):

	- step 1: adding the corresponding git tag:

		``git tag -a v1.x.x -m 'the tag for the version number 1.x.x``

	- step 2: updated the latest number (with tag) to the source code

		``python main.py version_update	// updated the version if necessary``

- Generate the apipary.apib from latest apib files:

		python main.py compile

- Parameters for each command can be found with the **-h** option

- Using CLI to generate the html template for the specific apiary file:

	``aglio -i bulletin.apib -o ~/Desktop/bulletin.html``

### 2. Procedure:
- Modify the corresponding apiary file(s)
- Change the git tag & run version_update if necessary
- Compile to generate the latest apiary.apib
- git push to push the latest apipary.apib to the main branch

### Resources:

- Download the erditor [Atom](https://atom.io/)
- Download the apiary rendering package for Atom with the [instructions](https://atom.io/packages/api-blueprint-preview)
