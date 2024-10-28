import React from "react"
import {
  Button,
  Form,
  Input,
  InputNumber,
  Select,
  DatePicker,
  Row,
  Col,
} from "antd"
import { useAppDispatch } from "../app/hooks"
import { createNewSearch } from "../features/searchSlice"

const { Option } = Select

const SearchForm: React.FC = () => {
  const dispatch = useAppDispatch()
  const [form] = Form.useForm()

  const onFinish = (values: any) => {
    dispatch(createNewSearch(values))
    // form.resetFields();
  }

  return (
    <Form form={form} onFinish={onFinish} layout="vertical">
      <Row gutter={16}>
        <Col span={12}>
          <Form.Item name="text" label="Text">
            <Input />
          </Form.Item>
        </Col>
        <Col span={12}>
          <Form.Item name="file_mask" label="File Mask">
            <Input />
          </Form.Item>
        </Col>
      </Row>
      <Row gutter={16}>
        <Col span={12}>
          <Form.Item name={["size", "value"]} label="File Size">
            <InputNumber style={{ width: "100%" }} />
          </Form.Item>
        </Col>
        <Col span={12}>
          <Form.Item name={["size", "operator"]} label="Size Operator">
            <Select>
              <Option value="gt">Greater than</Option>
              <Option value="lt">Less than</Option>
              <Option value="ge">Greater or Equal</Option>
              <Option value="le">Less or Equal</Option>
              <Option value="eq">Equal</Option>
            </Select>
          </Form.Item>
        </Col>
      </Row>
      <Row gutter={16}>
        <Col span={12}>
          <Form.Item name={["creation_time", "value"]} label="Creation Time">
            <DatePicker showTime style={{ width: "100%" }} />
          </Form.Item>
        </Col>
        <Col span={12}>
          <Form.Item
            name={["creation_time", "operator"]}
            label="Creation Operator"
          >
            <Select>
              <Option value="gt">After</Option>
              <Option value="lt">Before</Option>
              <Option value="ge">After or Exact</Option>
              <Option value="le">Before or Exact</Option>
              <Option value="eq">Exact</Option>
            </Select>
          </Form.Item>
        </Col>
      </Row>
      <Row justify="end">
        <Button type="primary" htmlType="submit">
          Start Search
        </Button>
      </Row>
    </Form>
  )
}

export default SearchForm
