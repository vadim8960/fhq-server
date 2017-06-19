#include "../headers/cmd_input_def.h"
#include <QJsonDocument>
#include <QJsonObject>

CmdInputDef::CmdInputDef(QString name){
	m_sName = name;
}

// ---------------------------------------------------------------------

CmdInputDef::CmdInputDef(){
}

// ---------------------------------------------------------------------

CmdInputDef & CmdInputDef::optional(){
	m_sRestrict = "optional";
	return *this;
}

// ---------------------------------------------------------------------

CmdInputDef & CmdInputDef::required(){
	m_sRestrict = "required";
	return *this;
}

// ---------------------------------------------------------------------

CmdInputDef & CmdInputDef::string_(){
	m_sType = "string";
	return *this;
}

// ---------------------------------------------------------------------

CmdInputDef & CmdInputDef::integer_(){
	m_sType = "integer";
	return *this;
}

// ---------------------------------------------------------------------

CmdInputDef & CmdInputDef::bool_(){
	m_sType = "boolean";
	return *this;
}
