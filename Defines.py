import enum

DATE_FORMAT = "%m/%d/%Y"
BASE_FOLDER_ADDRESS = "/Users/samhachem99/Library/Mobile Documents/com~apple~CloudDocs/Documents/Life/Financials/Records/"

FILTER_OUT_STRINGS = ["AplPay", "Merchandise & Supplies-", "Restaurant-"]

class SearchNodeElementSearchType(int, enum.Enum):
    SEARCH_NODE_ELEMENT_TYPE_EXACT_MATCH = 1,
    SEARCH_NODE_ELEMENT_TYPE_PARTIAL_MATCH = 2

class SearchNodeType(str, enum.Enum):
    SEARCH_NODE_TYPE_PRIMARY = "CAT"
    SEARCH_NODE_TYPE_SECONDARY = "SUB"

    def __str__(self):
        return str(self.value)

class SearchNodeDateConstraint(str, enum.Enum):
    SEARCH_NODE_DATE_CONSTRAINT_WEEKDAY = "Weekday"
    SEARCH_NODE_DATE_CONSTRAINT_WEEKEND = "Weekend"
    SEARCH_NODE_DATE_CONSTRAINT_BOTH = "Any Day"

    def __str__(self):
        return str(self.value)

class SearchNodeName(str, enum.Enum):
    SEARCH_NODE_NAME_HOME = "Home"
    SEARCH_NODE_NAME_BILLS = "Bills"
    SEARCH_NODE_NAME_SUBSCRIPTIONS = "Subscriptions"
    SEARCH_NODE_NAME_FOOD = "Food"
    SEARCH_NODE_NAME_GROCERIES = "Groceries"
    SEARCH_NODE_NAME_TRANSPORTATION = "Transportation"
    SEARCH_NODE_NAME_SHOPPING = "Shopping"
    SEARCH_NODE_NAME_ENTERTAINMENT = "Entertainment"
    SEARCH_NODE_NAME_PERSONAL = "Personal Expenses"
    SEARCH_NODE_NAME_FEES = "Fees"
    SEARCH_NODE_NAME_MISC = "Misc"

    SEARCH_NODE_NAME_FOOD_TI_FOOD = "Food::TI Food"
    SEARCH_NODE_NAME_FOOD_TI_SNACKS = "Food::TI Snacks"
    SEARCH_NODE_NAME_FOOD_WEEKDAY = "Food::Weekday"
    SEARCH_NODE_NAME_FOOD_WEEKEND = "Food::Weekend"

    SEARCH_NODE_NAME_GROCERIES_COSTCO = "Groceries::Costco"
    SEARCH_NODE_NAME_GROCERIES_OTHER = "Groceries::Other"

    SEARCH_NODE_NAME_TRANSPORTATION_GAS = "Transportation::Gas"
    SEARCH_NODE_NAME_TRANSPORTATION_TOLLS = "Transportation::Tolls"
    SEARCH_NODE_NAME_TRANSPORTATION_OTHER = "Transportation::Other"

    SEARCH_NODE_NAME_SHOPPING_ONLINE = "Shopping::Online"
    SEARCH_NODE_NAME_SHOPPING_CLOTHS = "Shopping::Cloths"
    SEARCH_NODE_NAME_SHOPPING_OTHER = "Shopping::Other"

    SEARCH_NODE_NAME_FEES_CC_FEES = "Fees::CC Fees"
    SEARCH_NODE_NAME_FEES_INTEREST = "Fees::Interest"
    SEARCH_NODE_NAME_FEES_OTHER = "Fees::Other"

    def __str__(self):
        return str(self.value)

class SearchNodeResultScore(int, enum.Enum):
    SEARCH_NODE_RESULT_SCORE_CAT_BOTH = 10
    SEARCH_NODE_RESULT_SCORE_DESC_BOTH = 20

    SEARCH_NODE_RESULT_SCORE_CAT_WEEKEDAY = 11
    SEARCH_NODE_RESULT_SCORE_CAT_WEEKEND = 12

    SEARCH_NODE_RESULT_SCORE_DESC_WEEKDAY = 21
    SEARCH_NODE_RESULT_SCORE_DESC_WEEKEND = 22

    def __str__(self):
        return self.value

# Sub categories
ti_food_node = {
    "node_name": SearchNodeName.SEARCH_NODE_NAME_FOOD_TI_FOOD,
    "node_type": SearchNodeType.SEARCH_NODE_TYPE_SECONDARY,
    "category": {
        "keywords": [],
        "exceptions": []
    },
    "Description": {
        "keywords": ["TEXAS INSTRUMENTS DADALLAS TX", "AplPay TEXAS INSTRUMDALLAS TX"],
        "exceptions": []
    },
    "sub": [],
    "time_constraints": SearchNodeDateConstraint.SEARCH_NODE_DATE_CONSTRAINT_BOTH,
    "expected_score": SearchNodeResultScore.SEARCH_NODE_RESULT_SCORE_DESC_BOTH,
    "total_amount": 0.0,
    "transaction_count": 0,
    "transactions": []
}

ti_snacks_node = {
    "node_name": SearchNodeName.SEARCH_NODE_NAME_FOOD_TI_SNACKS,
    "node_type": SearchNodeType.SEARCH_NODE_TYPE_SECONDARY,
    "category": {
        "keywords": [],
        "exceptions": []
    },
    "Description": {
        "keywords": ["AMERICAN FOOD N VENDI", "AMERICAN FOOD N VENDDALLAS TX"],
        "exceptions": []
    },
    "sub": [],
    "time_constraints": SearchNodeDateConstraint.SEARCH_NODE_DATE_CONSTRAINT_BOTH,
    "expected_score": SearchNodeResultScore.SEARCH_NODE_RESULT_SCORE_DESC_BOTH,
    "total_amount": 0.0,
    "transaction_count": 0,
    "transactions": []
}

food_weekday_node = {
    "node_name": SearchNodeName.SEARCH_NODE_NAME_FOOD_WEEKDAY,
    "node_type": SearchNodeType.SEARCH_NODE_TYPE_SECONDARY,
    "category": {
        "keywords": ["Restaurant-Restaurant", "Food & Drink", "Restaurant-Bar & Café"],
        "exceptions": []
    },
    "Description": {
        "keywords": [],
        "exceptions": ["TEXAS INSTRUMENTS DADALLAS TX", "AplPay TEXAS INSTRUMDALLAS TX", "AMERICAN FOOD N VENDI"],
    },
    "sub": [],
    "time_constraints": SearchNodeDateConstraint.SEARCH_NODE_DATE_CONSTRAINT_WEEKDAY,
    "expected_score": SearchNodeResultScore.SEARCH_NODE_RESULT_SCORE_CAT_WEEKEDAY,
    "total_amount": 0.0,
    "transaction_count": 0,
    "transactions": []
}

food_weekend_node = {
    "node_name": SearchNodeName.SEARCH_NODE_NAME_FOOD_WEEKEND,
    "node_type": SearchNodeType.SEARCH_NODE_TYPE_SECONDARY,
    "category": {
        "keywords": ["Restaurant-Restaurant", "Food & Drink", "Restaurant-Bar & Café"],
        "exceptions": []
    },
    "Description": {
        "keywords": [],
        "exceptions": ["TEXAS INSTRUMENTS DADALLAS TX", "AplPay TEXAS INSTRUMDALLAS TX", "AMERICAN FOOD N VENDI"],
    },
    "sub": [],
    "time_constraints": SearchNodeDateConstraint.SEARCH_NODE_DATE_CONSTRAINT_WEEKEND,
    "expected_score": SearchNodeResultScore.SEARCH_NODE_RESULT_SCORE_CAT_WEEKEND,
    "total_amount": 0.0,
    "transaction_count": 0,
    "transactions": []
}

groceries_costco_node = {
    "node_name": SearchNodeName.SEARCH_NODE_NAME_GROCERIES_COSTCO,
    "node_type": SearchNodeType.SEARCH_NODE_TYPE_SECONDARY,
    "category": {
        "keywords": [],
        "exceptions": []
    },
    "Description": {
        "keywords": ["COSTCO WHSE"],
        "exceptions": []
    },
    "sub": [],
    "time_constraints": SearchNodeDateConstraint.SEARCH_NODE_DATE_CONSTRAINT_BOTH,
    "expected_score": SearchNodeResultScore.SEARCH_NODE_RESULT_SCORE_DESC_BOTH,
    "total_amount": 0.0,
    "transaction_count": 0,
    "transactions": []
}

groceries_other_node = {
    "node_name": SearchNodeName.SEARCH_NODE_NAME_GROCERIES_OTHER,
    "node_type": SearchNodeType.SEARCH_NODE_TYPE_SECONDARY,
    "category": {
        "keywords": ["Groceries"],
        "exceptions": []
    },
    "Description": {
        "keywords": [],
        "exceptions": ["TEXAS INSTRUMENTS DADALLAS TX", "AplPay TEXAS INSTRUMDALLAS TX", "AMERICAN FOOD N VENDI", "AMERICAN FOOD N VENDDALLAS TX"]
    },
    "sub": [],
    "time_constraints": SearchNodeDateConstraint.SEARCH_NODE_DATE_CONSTRAINT_BOTH,
    "expected_score": SearchNodeResultScore.SEARCH_NODE_RESULT_SCORE_CAT_BOTH,
    "total_amount": 0.0,
    "transaction_count": 0,
    "transactions": []
}

gas_node = {
    "node_name": SearchNodeName.SEARCH_NODE_NAME_TRANSPORTATION_GAS,
    "node_type": SearchNodeType.SEARCH_NODE_TYPE_SECONDARY,
    "category": {
        "keywords": ["GAS", "Fuel"],
        "exceptions": []
    },
    "Description": {
        "keywords": [],
        "exceptions": [],
    },
    "sub": [],
    "time_constraints": SearchNodeDateConstraint.SEARCH_NODE_DATE_CONSTRAINT_BOTH,
    "expected_score": SearchNodeResultScore.SEARCH_NODE_RESULT_SCORE_CAT_BOTH,
    "total_amount": 0.0,
    "transaction_count": 0,
    "transactions": []
}

tolls_node = {
    "node_name": SearchNodeName.SEARCH_NODE_NAME_TRANSPORTATION_TOLLS,
    "node_type": SearchNodeType.SEARCH_NODE_TYPE_SECONDARY,
    "category": {
        "keywords": ["Travel"],
        "exceptions": []
    },
    "Description": {
        "keywords": ["NTTA AUTOCHARGE", "DFW AIRPORT"],
        "exceptions": [],
    },
    "sub": [],
    "time_constraints": SearchNodeDateConstraint.SEARCH_NODE_DATE_CONSTRAINT_BOTH,
    "expected_score": SearchNodeResultScore.SEARCH_NODE_RESULT_SCORE_DESC_BOTH,
    "total_amount": 0.0,
    "transaction_count": 0,
    "transactions": []
}

fees_cc_node = {
    "node_name": SearchNodeName.SEARCH_NODE_NAME_FEES_CC_FEES,
    "node_type": SearchNodeType.SEARCH_NODE_TYPE_SECONDARY,
    "category": {
        "keywords": [],
        "exceptions": []
    },
    "Description": {
        "keywords": ["RENEWAL MEMBERSHIP FEE"],
        "exceptions": [],
    },
    "sub": [],
    "time_constraints": SearchNodeDateConstraint.SEARCH_NODE_DATE_CONSTRAINT_BOTH,
    "expected_score": SearchNodeResultScore.SEARCH_NODE_RESULT_SCORE_DESC_BOTH,
    "total_amount": 0.0,
    "transaction_count": 0,
    "transactions": []
}

fees_interest_node = {
    "node_name": SearchNodeName.SEARCH_NODE_NAME_FEES_INTEREST,
    "node_type": SearchNodeType.SEARCH_NODE_TYPE_SECONDARY,
    "category": {
        "keywords": [],
        "exceptions": []
    },
    "Description": {
        "keywords": ["PURCHASE INTEREST"],
        "exceptions": [],
    },
    "sub": [],
    "time_constraints": SearchNodeDateConstraint.SEARCH_NODE_DATE_CONSTRAINT_BOTH,
    "expected_score": SearchNodeResultScore.SEARCH_NODE_RESULT_SCORE_DESC_BOTH,
    "total_amount": 0.0,
    "transaction_count": 0,
    "transactions": []
}

# Main Category
bills_node = {
    "node_name": SearchNodeName.SEARCH_NODE_NAME_BILLS,
    "node_type": SearchNodeType.SEARCH_NODE_TYPE_PRIMARY,
    "category": {
        "keywords": ["Insurance Services"],
        "exceptions": []
    },
    "Description": {
        "keywords": ["AT&T", "GEICO", "AMBIT", "KINDLE"],
        "exceptions": ["Fabletics"]
    },
    "sub": [],
    "time_constraints": SearchNodeDateConstraint.SEARCH_NODE_DATE_CONSTRAINT_BOTH,
    "expected_score": SearchNodeResultScore.SEARCH_NODE_RESULT_SCORE_CAT_BOTH,
    "total_amount": 0.0,
    "transaction_count": 0,
    "transactions": []
}

subscriptions_node = {
    "node_name": SearchNodeName.SEARCH_NODE_NAME_SUBSCRIPTIONS,
    "node_type": SearchNodeType.SEARCH_NODE_TYPE_PRIMARY,
    "category": {
        "keywords": [],
        "exceptions": []
    },
    "Description": {
        "keywords": ["Amazon Prime", "BARRON"],
        "exceptions": []
    },
    "sub": [],
    "time_constraints": SearchNodeDateConstraint.SEARCH_NODE_DATE_CONSTRAINT_BOTH,
    "expected_score": SearchNodeResultScore.SEARCH_NODE_RESULT_SCORE_DESC_BOTH,
    "total_amount": 0.0,
    "transaction_count": 0,
    "transactions": []
}

food_node = {
    "node_name": SearchNodeName.SEARCH_NODE_NAME_FOOD,
    "node_type": SearchNodeType.SEARCH_NODE_TYPE_PRIMARY,
    "category": {
        "keywords": ["Restaurant-Restaurant", "Food & Drink", "Restaurant-Bar & Café"],
        "exceptions": []
    },
    "Description": {
        "keywords": ["AMERICAN FOOD N VENDDALLAS TX"],
        "exceptions": []
    },
    "sub": [
        ti_food_node,
        ti_snacks_node,
        food_weekday_node,
        food_weekend_node,
    ],
    "time_constraints": SearchNodeDateConstraint.SEARCH_NODE_DATE_CONSTRAINT_BOTH,
    "expected_score": SearchNodeResultScore.SEARCH_NODE_RESULT_SCORE_CAT_BOTH,
    "total_amount": 0.0,
    "transaction_count": 0,
    "transactions": []
}

groceries_node = {
    "node_name": SearchNodeName.SEARCH_NODE_NAME_GROCERIES,
    "node_type": SearchNodeType.SEARCH_NODE_TYPE_PRIMARY,
    "category": {
        "keywords": ["Groceries", "Pharmacies"],
        "exceptions": []
    },
    "Description": {
        "keywords": ["COSTCO WHSE"],
        "exceptions": ["TEXAS INSTRUMENTS DADALLAS TX", "AplPay TEXAS INSTRUMDALLAS TX", "AMERICAN FOOD N VENDI", "AMERICAN FOOD N VENDDALLAS TX"]
    },
    "sub": [
        groceries_costco_node,
        groceries_other_node,
    ],
    "time_constraints": SearchNodeDateConstraint.SEARCH_NODE_DATE_CONSTRAINT_BOTH,
    "expected_score": SearchNodeResultScore.SEARCH_NODE_RESULT_SCORE_CAT_BOTH,
    "total_amount": 0.0,
    "transaction_count": 0,
    "transactions": []
}

transportation_node = {
    "node_name": SearchNodeName.SEARCH_NODE_NAME_TRANSPORTATION,
    "node_type": SearchNodeType.SEARCH_NODE_TYPE_PRIMARY,
    "category": {
        "keywords": ["Travel", "Gas", "Transportation", "Fuel"],
        "exceptions": []
    },
    "Description": {
        "keywords": ["DFW AIRPORT", "UBER"],
        "exceptions": ["UBER EATS"]
    },
    "sub": [
        gas_node,
        tolls_node,
    ],
    "time_constraints": SearchNodeDateConstraint.SEARCH_NODE_DATE_CONSTRAINT_BOTH,
    "expected_score": SearchNodeResultScore.SEARCH_NODE_RESULT_SCORE_CAT_BOTH,
    "total_amount": 0.0,
    "transaction_count": 0,
    "transactions": []
}

shopping_node = {
    "node_name": SearchNodeName.SEARCH_NODE_NAME_SHOPPING,
    "node_type": SearchNodeType.SEARCH_NODE_TYPE_PRIMARY,
    "category": {
        "keywords": ["Shopping", "Internet Purchase", "Sporting Goods Stores", "General Retail", "Book Stores", "Office Supplies"],
        "exceptions": []
    },
    "Description": {
        "keywords": ["FABLETICS"],
        "exceptions": ["COSTCO", "KINDLE"]
    },
    "sub": [],
    "time_constraints": SearchNodeDateConstraint.SEARCH_NODE_DATE_CONSTRAINT_BOTH,
    "expected_score": SearchNodeResultScore.SEARCH_NODE_RESULT_SCORE_CAT_BOTH,
    "total_amount": 0.0,
    "transaction_count": 0,
    "transactions": []
}

entertainment_node = {
    "node_name": SearchNodeName.SEARCH_NODE_NAME_ENTERTAINMENT,
    "node_type": SearchNodeType.SEARCH_NODE_TYPE_PRIMARY,
    "category": {
        "keywords": ["Entertainment", "Computer Supplies"],
        "exceptions": []
    },
    "Description": {
        "keywords": [],
        "exceptions": []
    },
    "sub": [],
    "time_constraints": SearchNodeDateConstraint.SEARCH_NODE_DATE_CONSTRAINT_BOTH,
    "expected_score": SearchNodeResultScore.SEARCH_NODE_RESULT_SCORE_CAT_BOTH,
    "total_amount": 0.0,
    "transaction_count": 0,
    "transactions": []
}

personal_node = {
    "node_name": SearchNodeName.SEARCH_NODE_NAME_PERSONAL,
    "node_type": SearchNodeType.SEARCH_NODE_TYPE_PRIMARY,
    "category": {
        "keywords": [],
        "exceptions": []
    },
    "Description": {
        "keywords": ["GREAT CL"],
        "exceptions": []
    },
    "sub": [],
    "time_constraints": SearchNodeDateConstraint.SEARCH_NODE_DATE_CONSTRAINT_BOTH,
    "expected_score": SearchNodeResultScore.SEARCH_NODE_RESULT_SCORE_CAT_BOTH,
    "total_amount": 0.0,
    "transaction_count": 0,
    "transactions": []
}

fees_node = {
    "node_name": SearchNodeName.SEARCH_NODE_NAME_FEES,
    "node_type": SearchNodeType.SEARCH_NODE_TYPE_PRIMARY,
    "category": {
        "keywords": ["Fees"],
        "exceptions": ["Transportation"]
    },
    "Description": {
        "keywords": ["PURCHASE INTEREST CHARGE"],
        "exceptions": []
    },
    "sub": [],
    "time_constraints": SearchNodeDateConstraint.SEARCH_NODE_DATE_CONSTRAINT_BOTH,
    "expected_score": SearchNodeResultScore.SEARCH_NODE_RESULT_SCORE_CAT_BOTH,
    "total_amount": 0.0,
    "transaction_count": 0,
    "transactions": []
}

misc_node = {
    "node_name": SearchNodeName.SEARCH_NODE_NAME_MISC,
    "node_type": SearchNodeType.SEARCH_NODE_TYPE_PRIMARY,
    "category": {
        "keywords": [],
        "exceptions": []
    },
    "Description": {
        "keywords": [],
        "exceptions": []
    },
    "sub": [],
    "time_constraints": SearchNodeDateConstraint.SEARCH_NODE_DATE_CONSTRAINT_BOTH,
    "expected_score": SearchNodeResultScore.SEARCH_NODE_RESULT_SCORE_CAT_BOTH,
    "total_amount": 0.0,
    "transaction_count": 0,
    "transactions": []
}

categoryNodes = [
    bills_node,
    subscriptions_node,
    food_node,
    groceries_node,
    transportation_node,
    shopping_node,
    entertainment_node,
    personal_node,
    fees_node,
]

subCategoryNodes = [
    ti_food_node,
    ti_snacks_node,
    food_weekday_node,
    food_weekend_node,
    groceries_costco_node,
    groceries_other_node,
    gas_node,
    tolls_node,
    fees_cc_node,
    fees_interest_node,
]

nodes = {
    "category": categoryNodes,
    "subCategory": subCategoryNodes,
}

nodes_list = [
    bills_node,
    subscriptions_node,
    food_node,
    groceries_node,
    transportation_node,
    shopping_node,
    entertainment_node,
    personal_node,
    fees_node,
    ti_food_node,
    ti_snacks_node,
    food_weekday_node,
    food_weekend_node,
    groceries_costco_node,
    groceries_other_node,
    gas_node,
    tolls_node,
    fees_cc_node,
    fees_interest_node,
]

output_dict = {
    "total_amount": 0.0,
    "transaction_count": 0,
    "transaction_hits": 0,
    "nodes": [],
    "no_hit_transactions": [],
    "multi_hit_transactions": []
}