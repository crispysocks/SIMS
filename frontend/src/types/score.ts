export interface Score {
  student_no: string
  exam_no: number
  exam_name: string
  score: number
  exam_date?: string
  remark?: string
  isdeleted?: number
}

export interface ScoreCreate {
  student_no: string
  exam_no: number
  exam_name: string
  score: number
  exam_date?: string
  remark?: string
}

export interface ScoreUpdate {
  student_no: string
  exam_no: number
  exam_name: string
  score: number
  exam_date?: string
  remark?: string
}